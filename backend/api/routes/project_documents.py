"""Project-scoped document API endpoints.

Routes follow GitHub-style URL structure:
  /api/v1/{organization_slug}/{project_slug}/documents
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Document, Folder, Organization, Project, User
from shared.db.session import get_db_dependency
from shared.schemas.document import (
    DocumentCreate,
    DocumentListItem,
    DocumentListResponse,
    DocumentResponse,
    DocumentUpdate,
    FolderTreeItem,
    generate_slug,
)
from shared.utils.pagination import apply_pagination, build_pagination_response
from shared.utils.logging import get_logger

logger = get_logger(__name__)

SessionDep = Annotated[Session, Depends(get_db_dependency)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(tags=["project-documents"])


def get_project_by_slugs(
    session: Session,
    organization_slug: str,
    project_slug: str,
    current_user: User | None = None,
) -> Project:
    """Get project by organization and project slugs with optional user validation."""
    # Get organization
    org = session.execute(
        select(Organization).where(Organization.slug == organization_slug)
    ).scalar_one_or_none()

    if not org:
        logger.warning(
            "Organization not found",
            organization_slug=organization_slug,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization '{organization_slug}' not found",
        )

    # Get project within organization
    project = session.execute(
        select(Project).where(
            Project.organization_id == org.id,
            Project.slug == project_slug,
        )
    ).scalar_one_or_none()

    if not project:
        logger.warning(
            "Project not found",
            organization_slug=organization_slug,
            project_slug=project_slug,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_slug}' not found in organization '{organization_slug}'",
        )

    # Optional: validate user has access
    if current_user and org.created_by != current_user.id:
        logger.warning(
            "Access denied to project",
            project_id=str(project.id),
            user_id=str(current_user.id),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this project",
        )

    return project


@router.get(
    "/{organization_slug}/{project_slug}/documents/tree",
    response_model=list[FolderTreeItem],
)
def get_project_document_tree(
    organization_slug: str,
    project_slug: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> list[FolderTreeItem]:
    """Get hierarchical tree structure of folders and documents for a specific project."""
    logger.info(
        "Getting document tree for project",
        organization_slug=organization_slug,
        project_slug=project_slug,
        user_id=str(current_user.id),
    )

    # Get project (validates access)
    project = get_project_by_slugs(session, organization_slug, project_slug, current_user)

    # Get all documents for this project with folder info
    documents = session.execute(
        select(Document)
        .outerjoin(Folder, Document.folder_id == Folder.id)
        .where(Document.project_id == project.id)
    ).scalars().all()

    # Build tree structure
    class TreeNode:
        def __init__(self, name: str, path: str):
            self.name = name
            self.path = path
            self.documents: list[Document] = []
            self.children: dict[str, "TreeNode"] = {}

    root = TreeNode("", "")

    for doc in documents:
        folder_path = None
        if doc.folder_id:
            folder = session.execute(
                select(Folder).where(Folder.id == doc.folder_id)
            ).scalar_one_or_none()
            if folder:
                folder_path = folder.path

        # If no folder_id, try to infer from filename
        if not folder_path and doc.filename:
            filename_parts = doc.filename.split("/")
            if len(filename_parts) > 1:
                folder_path = "/".join(filename_parts[:-1])

        if not folder_path:
            # Document at root level
            root.documents.append(doc)
        else:
            # Navigate/create path
            parts = folder_path.split("/")
            current = root
            current_path = ""

            for part in parts:
                if current_path:
                    current_path += "/"
                current_path += part

                if part not in current.children:
                    current.children[part] = TreeNode(part, current_path)

                current = current.children[part]

            current.documents.append(doc)

    # Convert TreeNode to FolderTreeItem
    def convert_node(node: TreeNode) -> list[FolderTreeItem]:
        items: list[FolderTreeItem] = []

        # Add child folders first
        for child_name, child_node in sorted(node.children.items()):
            items.append(FolderTreeItem(
                type="folder",
                id=child_node.path,
                name=child_name,
                path=child_node.path,
                slug=None,
                children=convert_node(child_node)
            ))

        # Add documents at this level after folders
        for doc in node.documents:
            items.append(FolderTreeItem(
                type="document",
                id=str(doc.id),
                name=doc.title,
                path=doc.filename,
                slug=doc.slug,
                children=[]
            ))

        return items

    return convert_node(root)


@router.get(
    "/{organization_slug}/{project_slug}/documents",
    response_model=DocumentListResponse,
)
def list_project_documents(
    organization_slug: str,
    project_slug: str,
    session: SessionDep,
    current_user: CurrentUserDep,
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=25, ge=1, le=100, description="Items per page"),
    sort_by: str = Query(default="updated_at", description="Field to sort by"),
    order: str = Query(default="desc", pattern="^(asc|desc)$", description="Sort order"),
) -> dict:
    """List documents for a specific project with pagination."""
    logger.info(
        "Listing documents for project",
        organization_slug=organization_slug,
        project_slug=project_slug,
        user_id=str(current_user.id),
    )

    # Get project (validates access)
    project = get_project_by_slugs(session, organization_slug, project_slug, current_user)

    # Build query scoped to project
    query = (
        select(Document)
        .outerjoin(Folder, Document.folder_id == Folder.id)
        .where(Document.project_id == project.id)
    )

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
    items = []
    for doc in documents:
        folder_name = None
        folder_path = None
        if doc.folder_id:
            folder = session.execute(
                select(Folder).where(Folder.id == doc.folder_id)
            ).scalar_one_or_none()
            if folder:
                folder_name = folder.name
                folder_path = folder.path

        items.append(
            DocumentListItem(
                id=doc.id,
                title=doc.title,
                slug=doc.slug,
                filename=doc.filename,
                rating=doc.rating,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
                folder_id=doc.folder_id,
                folder_name=folder_name,
                folder_path=folder_path,
            )
        )

    return build_pagination_response(items, page, per_page, total, total_pages)


@router.post(
    "/{organization_slug}/{project_slug}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_document(
    organization_slug: str,
    project_slug: str,
    document_data: DocumentCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Document:
    """Create a new document within a specific project."""
    logger.info(
        "Creating document in project",
        organization_slug=organization_slug,
        project_slug=project_slug,
        title=document_data.title,
        user_id=str(current_user.id),
    )

    # Get project (validates access)
    project = get_project_by_slugs(session, organization_slug, project_slug, current_user)
    org = session.execute(
        select(Organization).where(Organization.slug == organization_slug)
    ).scalar_one()

    # Generate slug from title
    slug = generate_slug(document_data.title)

    # Check if slug already exists in this project
    existing = session.execute(
        select(Document).where(
            Document.project_id == project.id,
            Document.slug == slug,
        )
    ).scalar_one_or_none()

    if existing:
        logger.warning(
            "Document creation failed: slug already exists in project",
            slug=slug,
            project_id=str(project.id),
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Document with slug '{slug}' already exists in this project",
        )

    # Create document
    document = Document(
        title=document_data.title,
        slug=slug,
        content=document_data.content,
        filename=document_data.filename,
        project_id=project.id,
        organization_id=org.id,
        folder_id=None,
        rating=None,
        created_by=current_user.id,
        updated_by=current_user.id,
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    logger.info(
        "Document created successfully",
        document_id=str(document.id),
        slug=document.slug,
    )

    return document


@router.get(
    "/{organization_slug}/{project_slug}/documents/slug/{slug}",
    response_model=DocumentResponse,
)
def get_project_document_by_slug(
    organization_slug: str,
    project_slug: str,
    slug: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Document:
    """Get a document by slug within a specific project."""
    logger.info(
        "Getting document by slug",
        organization_slug=organization_slug,
        project_slug=project_slug,
        slug=slug,
        user_id=str(current_user.id),
    )

    # Get project (validates access)
    project = get_project_by_slugs(session, organization_slug, project_slug, current_user)

    # Get document within project
    document = session.execute(
        select(Document).where(
            Document.project_id == project.id,
            Document.slug == slug,
        )
    ).scalar_one_or_none()

    if not document:
        logger.warning(
            "Document not found",
            slug=slug,
            project_id=str(project.id),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with slug '{slug}' not found in this project",
        )

    return document
