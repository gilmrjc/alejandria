"""Document API endpoints with CRUD operations, pessimistic locking, and versioning."""

import time
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Document, DocumentSnapshot, Organization, Project, User
from shared.db.session import get_db_session
from shared.schemas.document import (
    DocumentCreate,
    DocumentListItem,
    DocumentListResponse,
    DocumentResponse,
    DocumentUpdate,
    generate_slug,
)
from shared.utils.pagination import apply_pagination, build_pagination_response

SessionDep = Annotated[Session, Depends(get_db_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/documents", tags=["documents"])


def acquire_document_lock(
    session: Session, document_id: uuid.UUID, max_retries: int = 3
) -> Document:
    """
    Acquire pessimistic lock on document with exponential backoff.

    Args:
        session: Database session
        document_id: Document ID to lock
        max_retries: Maximum number of retry attempts

    Returns:
        Locked document instance

    Raises:
        HTTPException: If lock cannot be acquired after retries
    """
    delays = [0.1, 0.5, 1.0]  # Exponential backoff delays in seconds

    for attempt in range(max_retries):
        try:
            # Acquire lock with SELECT FOR UPDATE
            document = session.execute(
                select(Document).where(Document.id == document_id).with_for_update()
            ).scalar_one()

            return document

        except SQLAlchemyError as e:
            if attempt < max_retries - 1:
                delay = delays[min(attempt, len(delays) - 1)]
                time.sleep(delay)
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        "Document is currently being modified by another operation. "
                        "Please try again."
                    ),
                ) from e


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(
    document_data: DocumentCreate,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Document:
    """
    Create a new document.

    Side effects:
    - Enqueues gap_detection job (to be implemented in T-023)
    """
    # Generate slug from title
    slug = generate_slug(document_data.title)

    # Check if slug already exists
    existing = session.execute(
        select(Document).where(Document.slug == slug)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Document with slug '{slug}' already exists",
        )

    # Get user's default organization and project
    # For MVP, use the first organization/project the user has access to
    organization = session.execute(
        select(Organization).where(Organization.created_by == current_user.id)
    ).scalars().first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization to create documents",
        )

    project = session.execute(
        select(Project).where(
            Project.organization_id == organization.id,
            Project.created_by == current_user.id,
        )
    ).scalars().first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have a project to create documents",
        )

    # Create document with auth context
    document = Document(
        title=document_data.title,
        slug=slug,
        content=document_data.content,
        filename=document_data.filename,
        project_id=project.id,
        organization_id=organization.id,
        folder_id=None,
        rating=None,
        created_by=current_user.id,
        updated_by=current_user.id,
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    return document


@router.get("/slug/{slug}", response_model=DocumentResponse)
def get_document_by_slug(
    slug: str,
    session: Annotated[Session, Depends(get_db_session)],
) -> Document:
    """Get a document by slug."""
    document = session.execute(
        select(Document).where(Document.slug == slug)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    return document


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db_session)],
) -> Document:
    """Get a document by ID."""
    document = session.execute(
        select(Document).where(Document.id == document_id)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    return document


@router.get("", response_model=DocumentListResponse)
def list_documents(
    session: Annotated[Session, Depends(get_db_session)],
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=25, ge=1, le=100, description="Items per page"),
    updated_after: datetime | None = Query(  # noqa: B008 - FastAPI pattern for optional query params with defaults
        default=None, description="Filter by update date"
    ),
    sort_by: str = Query(default="updated_at", description="Field to sort by"),
    order: str = Query(
        default="desc", pattern="^(asc|desc)$", description="Sort order"
    ),
) -> dict:
    """List documents with pagination and filtering."""
    # Build query
    query = select(Document)

    # Apply filters
    if updated_after is not None:
        query = query.where(Document.updated_at >= updated_after)

    # Apply sorting
    sort_column = getattr(Document, sort_by, Document.updated_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    documents, total, total_pages = apply_pagination(
        query, session, page=page, per_page=per_page
    )

    # Convert to response format
    items = [
        DocumentListItem(
            id=doc.id,
            title=doc.title,
            slug=doc.slug,
            filename=doc.filename,
            rating=doc.rating,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )
        for doc in documents
    ]

    return build_pagination_response(items, page, per_page, total, total_pages)


@router.put("/slug/{slug}", response_model=DocumentResponse)
def update_document_by_slug(
    slug: str,
    document_data: DocumentUpdate,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Document:
    """
    Update a document by slug with pessimistic locking.

    Side effects:
    - Creates automatic snapshot via middleware
    - Re-enqueues gap_detection job (to be implemented in T-023)
    """
    # Get document by slug
    document = session.execute(
        select(Document).where(Document.slug == slug)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Acquire pessimistic lock
    document = acquire_document_lock(session, document.id)

    # Update fields if provided
    if document_data.title is not None:
        document.title = document_data.title
        document.slug = generate_slug(document_data.title)

    if document_data.content is not None:
        document.content = document_data.content

    if document_data.filename is not None:
        document.filename = document_data.filename

    # Update metadata
    document.updated_by = current_user.id

    session.commit()
    session.refresh(document)

    return document


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: uuid.UUID,
    document_data: DocumentUpdate,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Document:
    """
    Update a document with pessimistic locking.

    Side effects:
    - Creates automatic snapshot via middleware
    - Re-enqueues gap_detection job (to be implemented in T-023)
    """
    # Acquire pessimistic lock
    document = acquire_document_lock(session, document_id)

    # Update fields if provided
    if document_data.title is not None:
        document.title = document_data.title
        document.slug = generate_slug(document_data.title)

    if document_data.content is not None:
        document.content = document_data.content

    if document_data.filename is not None:
        document.filename = document_data.filename

    document.updated_by = current_user.id

    # Commit (middleware will create snapshot automatically)
    session.commit()
    session.refresh(document)

    return document


@router.delete("/slug/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document_by_slug(
    slug: str,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Delete a document by slug.

    Side effects:
    - CASCADE DELETE of gaps, document_snapshots
    - Cancels active related jobs (to be implemented in T-023)
    """
    document = session.execute(
        select(Document).where(Document.slug == slug)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    session.delete(document)
    session.commit()


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Delete a document.

    Side effects:
    - CASCADE DELETE of gaps, document_snapshots
    - Cancels active related jobs (to be implemented in T-023)
    """
    document = session.execute(
        select(Document).where(Document.id == document_id)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    session.delete(document)
    session.commit()


@router.get("/slug/{slug}/snapshots", response_model=dict)
def list_document_snapshots_by_slug(
    slug: str,
    session: Annotated[Session, Depends(get_db_session)],
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=25, ge=1, le=100, description="Items per page"),
) -> dict:
    """Get snapshots for a document by slug."""
    # Verify document exists
    document = session.execute(
        select(Document).where(Document.slug == slug)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Get snapshots
    query = (
        select(DocumentSnapshot)
        .where(DocumentSnapshot.document_id == document.id)
        .order_by(DocumentSnapshot.created_at.desc())
    )

    # Apply pagination
    snapshots, total, total_pages = apply_pagination(
        query, session, page=page, per_page=per_page
    )

    items = [
        {
            "id": snap.id,
            "document_id": snap.document_id,
            "content": snap.new_content,
            "created_at": snap.created_at,
            "created_by": snap.created_by,
        }
        for snap in snapshots
    ]

    return build_pagination_response(items, page, per_page, total, total_pages)


@router.get("/{document_id}/snapshots", response_model=dict)
def list_document_snapshots(
    document_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db_session)],
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=25, ge=1, le=100, description="Items per page"),
) -> dict:
    """Get snapshots for a document."""
    # Verify document exists
    document = session.execute(
        select(Document).where(Document.id == document_id)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Get snapshots
    query = (
        select(DocumentSnapshot)
        .where(DocumentSnapshot.document_id == document_id)
        .order_by(DocumentSnapshot.created_at.desc())
    )

    # Apply pagination
    snapshots, total, total_pages = apply_pagination(
        query, session, page=page, per_page=per_page
    )

    items = [
        {
            "id": snap.id,
            "document_id": snap.document_id,
            "content": snap.new_content,
            "created_at": snap.created_at,
            "created_by": snap.created_by,
        }
        for snap in snapshots
    ]

    return build_pagination_response(items, page, per_page, total, total_pages)


@router.post(
    "/slug/{slug}/snapshots/{snapshot_id}/restore", response_model=DocumentResponse
)
def restore_snapshot_by_slug(
    slug: str,
    snapshot_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Document:
    """
    Restore a document snapshot by slug.

    Side effects:
    - Creates snapshot of current state before restoring
    """
    # Get document by slug
    document = session.execute(
        select(Document).where(Document.slug == slug)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Get snapshot
    snapshot = session.execute(
        select(DocumentSnapshot).where(
            DocumentSnapshot.id == snapshot_id,
            DocumentSnapshot.document_id == document.id,
        )
    ).scalar_one_or_none()

    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Snapshot not found"
        )

    # Create snapshot of current state before restoring
    current_snapshot = DocumentSnapshot(
        document_id=document.id,
        new_content=document.content,
        created_by=current_user.id,
    )
    session.add(current_snapshot)

    # Restore content
    document.content = snapshot.new_content
    document.updated_by = current_user.id

    session.commit()
    session.refresh(document)

    return document


@router.post(
    "/{document_id}/snapshots/{snapshot_id}/restore", response_model=DocumentResponse
)
def restore_snapshot(
    document_id: uuid.UUID,
    snapshot_id: uuid.UUID,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Document:
    """
    Restore a document snapshot.

    Side effects:
    - Creates snapshot of current state before restoring
    """
    # Acquire pessimistic lock
    document = acquire_document_lock(session, document_id)

    # Get snapshot
    snapshot = session.execute(
        select(DocumentSnapshot).where(
            DocumentSnapshot.id == snapshot_id,
            DocumentSnapshot.document_id == document_id,
        )
    ).scalar_one_or_none()

    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Snapshot not found"
        )

    # Validate snapshot integrity
    if snapshot.old_content is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot restore snapshot with no old content",
        )

    # Store current content for snapshot

    # Restore content
    document.content = snapshot.old_content
    document.updated_by = current_user.id

    # Commit (middleware will create snapshot of current state)
    session.commit()
    session.refresh(document)

    return document
