"""Gap API endpoints with CRUD operations."""

import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from jobs.tasks.gap_detection import gap_detection_task
from jobs.tasks.question_generation import question_generation_task
from shared.auth.jwt import get_current_user

from shared.db.models import Document, Gap, GapDocumentReference, User
from shared.db.session import get_db_dependency

from shared.schemas.gap import (
    GapCreate,
    GapDashboardMetrics,
    GapDashboardResponse,
    GapListItem,
    GapListResponse,
    GapResponse,
    GapThemeCluster,
    GapUpdate,
)

from shared.services.gap_grouping_service import GapGroupingService
from shared.utils.pagination import apply_pagination, build_pagination_response

logger = logging.getLogger(__name__)

SessionDep = Annotated[Session, Depends(get_db_dependency)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/gaps", tags=["gaps"])


@router.post("", response_model=GapResponse, status_code=status.HTTP_201_CREATED)
def create_gap(
    gap_data: GapCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Gap:
    """Create a new gap."""
    # Verify document exists
    document = session.execute(
        select(Document).where(Document.id == gap_data.document_id)
    ).scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Generate slug from question
    slug = gap_data.question.lower().replace(" ", "-")[:50]

    # Check if slug already exists
    existing = session.execute(select(Gap).where(Gap.slug == slug)).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Gap with slug '{slug}' already exists",
        )

    # Create gap
    gap = Gap(
        document_id=gap_data.document_id,
        slug=slug,
        question=gap_data.question,
        priority=gap_data.priority,
        context_missing=gap_data.context_missing,
        role_affected=gap_data.role_affected,
        status="pending",
    )

    session.add(gap)
    session.commit()
    session.refresh(gap)

    return gap


@router.get("/slug/{slug}", response_model=GapResponse)
def get_gap_by_slug(
    slug: str,
    session: SessionDep,
) -> dict:
    """Get a gap by slug."""
    gap = session.execute(
        select(Gap).where(Gap.slug == slug)
    ).scalar_one_or_none()

    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gap not found"
        )

    # Get document information
    document = session.execute(
        select(Document).where(Document.id == gap.document_id)
    ).scalar_one_or_none()

    # Get reference documents
    gap_document_refs = session.execute(
        select(GapDocumentReference).where(GapDocumentReference.gap_id == gap.id)
    ).scalars().all()

    reference_document_ids = [gdr.document_id for gdr in gap_document_refs]
    reference_documents = []
    if reference_document_ids:
        ref_docs = session.execute(
            select(Document).where(Document.id.in_(reference_document_ids))
        ).scalars().all()
        reference_documents = [
            {
                "id": doc.id,
                "slug": doc.slug,
                "title": doc.title,
                "filename": doc.filename,
            }
            for doc in ref_docs
        ]

    # Build response with document info
    response = {
        "id": gap.id,
        "document_id": gap.document_id,
        "document_slug": document.slug if document else None,
        "document_title": document.title if document else None,
        "slug": gap.slug,
        "question": gap.question,
        "priority": gap.priority,
        "status": gap.status,
        "context_missing": gap.context_missing,
        "role_affected": gap.role_affected,
        "answer": gap.answer,
        "answered_at": gap.answered_at,
        "answered_by": gap.answered_by,
        "created_at": gap.created_at,
        "updated_at": gap.updated_at,
        "reference_documents": reference_documents,
    }

    return response


@router.get("/{gap_id}", response_model=GapResponse)
def get_gap(
    gap_id: uuid.UUID,
    session: SessionDep,
) -> dict:
    """Get a gap by ID."""
    gap = session.execute(select(Gap).where(Gap.id == gap_id)).scalar_one_or_none()

    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gap not found"
        )

    # Get document information
    document = session.execute(
        select(Document).where(Document.id == gap.document_id)
    ).scalar_one_or_none()

    # Build response with document info
    response = {
        "id": gap.id,
        "document_id": gap.document_id,
        "document_slug": document.slug if document else None,
        "document_title": document.title if document else None,
        "slug": gap.slug,
        "question": gap.question,
        "priority": gap.priority,
        "status": gap.status,
        "context_missing": gap.context_missing,
        "role_affected": gap.role_affected,
        "answer": gap.answer,
        "answered_at": gap.answered_at,
        "answered_by": gap.answered_by,
        "created_at": gap.created_at,
        "updated_at": gap.updated_at,
    }

    return response


@router.get("", response_model=GapListResponse)
def list_gaps(
    session: SessionDep,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    per_page: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 25,
    status: Annotated[str | None, Query(description="Filter by status")] = None,
    priority: Annotated[str | None, Query(description="Filter by priority")] = None,
    document_id: Annotated[
        uuid.UUID | None, Query(description="Filter by document")
    ] = None,
) -> dict:
    """List gaps with pagination and filtering."""
    # Build query
    query = select(Gap)

    # Apply filters
    if status is not None:
        query = query.where(Gap.status == status)

    if priority is not None:
        query = query.where(Gap.priority == priority)

    if document_id is not None:
        query = query.where(Gap.document_id == document_id)

    # Apply sorting (newest first)
    query = query.order_by(Gap.created_at.desc())

    # Apply pagination
    gaps, total, total_pages = apply_pagination(
        query, session, page=page, per_page=per_page
    )

    # Get all document IDs
    document_ids = [gap.document_id for gap in gaps]
    documents = {}
    if document_ids:
        docs = session.execute(
            select(Document).where(Document.id.in_(document_ids))
        ).scalars().all()
        documents = {doc.id: doc for doc in docs}

    # Convert to response format
    items = [
        GapListItem(
            id=gap.id,
            document_id=gap.document_id,
            document_slug=documents[gap.document_id].slug if gap.document_id in documents else None,
            document_title=documents[gap.document_id].title if gap.document_id in documents else None,
            slug=gap.slug,
            question=gap.question,
            priority=gap.priority,
            status=gap.status,
            created_at=gap.created_at,
        )
        for gap in gaps
    ]

    return build_pagination_response(items, page, per_page, total, total_pages)


@router.put("/slug/{slug}", response_model=GapResponse)
def update_gap_by_slug(
    slug: str,
    gap_data: GapUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Gap:
    """Update a gap by slug (answer and status)."""
    gap = session.execute(select(Gap).where(Gap.slug == slug)).scalar_one_or_none()

    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gap not found"
        )

    # Update fields if provided
    if gap_data.answer is not None:
        gap.answer = gap_data.answer

    if gap_data.status is not None:
        gap.status = gap_data.status
        if gap_data.status == "responded" and gap.answer:
            from datetime import UTC, datetime

            gap.answered_at = datetime.now(UTC)
            gap.answered_by = current_user.id

            try:
                question_generation_task.delay(str(gap.id), gap.answer)
            except Exception:
                logger.warning(f"Could not enqueue question_generation for gap {gap.id}")

    session.commit()
    session.refresh(gap)

    return gap


@router.put("/{gap_id}", response_model=GapResponse)
def update_gap(
    gap_id: uuid.UUID,
    gap_data: GapUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Gap:
    """Update a gap (answer and status)."""
    gap = session.execute(select(Gap).where(Gap.id == gap_id)).scalar_one_or_none()

    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gap not found"
        )

    # Update fields if provided
    if gap_data.answer is not None:
        gap.answer = gap_data.answer

    if gap_data.status is not None:
        gap.status = gap_data.status
        if gap_data.status == "responded" and gap.answer:
            from datetime import UTC, datetime

            gap.answered_at = datetime.now(UTC)
            gap.answered_by = current_user.id

            try:
                question_generation_task.delay(str(gap.id), gap.answer)
            except Exception:
                logger.warning(f"Could not enqueue question_generation for gap {gap.id}")

    session.commit()
    session.refresh(gap)

    return gap


@router.delete("/slug/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gap_by_slug(
    slug: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> None:
    """Delete a gap by slug."""
    gap = session.execute(select(Gap).where(Gap.slug == slug)).scalar_one_or_none()

    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gap not found"
        )

    session.delete(gap)
    session.commit()


@router.delete("/{gap_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gap(
    gap_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> None:
    """Delete a gap."""
    gap = session.execute(select(Gap).where(Gap.id == gap_id)).scalar_one_or_none()

    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gap not found"
        )

    session.delete(gap)
    session.commit()


@router.get("/dashboard", response_model=GapDashboardResponse)
def get_gap_dashboard(
    session: SessionDep,
    status: Annotated[str | None, Query(description="Filter by status")] = None,
    priority: Annotated[str | None, Query(description="Filter by priority")] = None,
    document_id: Annotated[
        uuid.UUID | None, Query(description="Filter by document")
    ] = None,
) -> dict:
    """Get gap dashboard metrics and theme clusters."""
    # Build query
    query = select(Gap)

    # Apply filters
    if status is not None:
        query = query.where(Gap.status == status)

    if priority is not None:
        query = query.where(Gap.priority == priority)

    if document_id is not None:
        query = query.where(Gap.document_id == document_id)

    # Execute query
    gaps = session.execute(query).scalars().all()

    # Calculate metrics
    total_gaps = len(gaps)
    by_status = {}
    by_priority = {}

    for gap in gaps:
        by_status[gap.status] = by_status.get(gap.status, 0) + 1
        by_priority[gap.priority] = by_priority.get(gap.priority, 0) + 1

    # Get theme clusters using GapGroupingService
    grouping_service = GapGroupingService(session)
    tag_clusters = grouping_service.group_gaps_by_tags()

    # Build theme clusters
    theme_clusters = []
    for theme, gap_dicts in tag_clusters.items():
        # Convert gap dicts to GapListItem
        gap_items = []
        for g in gap_dicts:
            # Get the actual gap to get created_at
            actual_gap = session.execute(
                select(Gap).where(Gap.id == uuid.UUID(g["id"]))
            ).scalar_one_or_none()
            created_at = actual_gap.created_at if actual_gap else None

            gap_items.append(
                GapListItem(
                    id=uuid.UUID(g["id"]),
                    document_id=uuid.UUID(g["document_id"]),
                    slug="",  # Not available in dict
                    question=g["question"],
                    priority=g["priority"],
                    status=g["status"],
                    created_at=created_at,
                )
            )
        theme_clusters.append(
            GapThemeCluster(theme=theme, count=len(gap_items), gaps=gap_items)
        )

    # Build metrics
    metrics = GapDashboardMetrics(
        total_gaps=total_gaps,
        by_status=by_status,
        by_priority=by_priority,
        by_theme={cluster.theme: cluster.count for cluster in theme_clusters},
    )

    return GapDashboardResponse(metrics=metrics, theme_clusters=theme_clusters)


@router.post("/detect-all", status_code=status.HTTP_202_ACCEPTED)
def detect_gaps_all_documents(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> dict:
    """
    Encola todos los documentos existentes para detección de gaps.

    Returns:
        Dict con información de las tareas encoladas
    """
    from shared.db.models import Document

    # Obtener todos los documentos
    documents = session.execute(select(Document)).scalars().all()

    if not documents:
        return {
            "message": "No documents found",
            "tasks_enqueued": 0,
            "tasks": [],
        }

    # Encolar tareas
    tasks = []
    for doc in documents:
        try:
            result = gap_detection_task.delay(str(doc.id))
            tasks.append(
                {
                    "document_id": str(doc.id),
                    "document_title": doc.title,
                    "task_id": result.id,
                }
            )
        except Exception as e:
            tasks.append(
                {
                    "document_id": str(doc.id),
                    "document_title": doc.title,
                    "error": str(e),
                }
            )

    return {
        "message": f"Enqueued {len([t for t in tasks if 'error' not in t])} documents for gap detection",
        "tasks_enqueued": len([t for t in tasks if "error" not in t]),
        "total_documents": len(documents),
        "tasks": tasks,
    }
