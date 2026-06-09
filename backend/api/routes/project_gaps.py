"""Project-scoped gap API endpoints.

Routes follow GitHub-style URL structure:
  /api/v1/{organization_slug}/{project_slug}/gaps
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Document, Gap, Organization, Project, User
from shared.db.session import get_db_dependency
from shared.schemas.gap import GapListItem, GapListResponse, GapResponse
from shared.utils.pagination import apply_pagination, build_pagination_response
from shared.utils.logging import get_logger

logger = get_logger(__name__)

SessionDep = Annotated[Session, Depends(get_db_dependency)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(tags=["project-gaps"])


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
    "/{organization_slug}/{project_slug}/gaps",
    response_model=GapListResponse,
)
def list_project_gaps(
    organization_slug: str,
    project_slug: str,
    session: SessionDep,
    current_user: CurrentUserDep,
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=25, ge=1, le=100, description="Items per page"),
    status_filter: str | None = Query(default=None, alias="status", description="Filter by status"),
    priority: str | None = Query(default=None, description="Filter by priority"),
    sort_by: str = Query(default="created_at", description="Field to sort by"),
    order: str = Query(default="desc", pattern="^(asc|desc)$", description="Sort order"),
) -> dict:
    """List gaps for a specific project with pagination and filtering."""
    logger.info(
        "Listing gaps for project",
        organization_slug=organization_slug,
        project_slug=project_slug,
        user_id=str(current_user.id),
    )

    # Get project (validates access)
    project = get_project_by_slugs(session, organization_slug, project_slug, current_user)

    # Build query scoped to project
    query = (
        select(Gap)
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id)
    )

    # Apply filters
    if status_filter:
        query = query.where(Gap.status == status_filter)
    if priority:
        query = query.where(Gap.priority == priority)

    # Apply sorting
    sort_column = getattr(Gap, sort_by, Gap.created_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    gaps, total, total_pages = apply_pagination(query, session, page=page, per_page=per_page)

    # Convert to response format
    items = []
    for gap in gaps:
        # Get document info
        doc = session.execute(
            select(Document).where(Document.id == gap.document_id)
        ).scalar_one_or_none()

        items.append(
            GapListItem(
                id=str(gap.id),
                slug=gap.slug,
                question=gap.question,
                priority=gap.priority,
                status=gap.status,
                document_slug=doc.slug if doc else None,
                document_title=doc.title if doc else None,
                created_at=gap.created_at,
                updated_at=gap.updated_at,
            )
        )

    return build_pagination_response(items, page, per_page, total, total_pages)


@router.get(
    "/{organization_slug}/{project_slug}/gaps/slug/{gap_slug}",
    response_model=GapResponse,
)
def get_project_gap_by_slug(
    organization_slug: str,
    project_slug: str,
    gap_slug: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Gap:
    """Get a gap by slug within a specific project."""
    logger.info(
        "Getting gap by slug",
        organization_slug=organization_slug,
        project_slug=project_slug,
        gap_slug=gap_slug,
        user_id=str(current_user.id),
    )

    # Get project (validates access)
    project = get_project_by_slugs(session, organization_slug, project_slug, current_user)

    # Get gap within project
    gap = session.execute(
        select(Gap)
        .join(Document, Gap.document_id == Document.id)
        .where(
            Document.project_id == project.id,
            Gap.slug == gap_slug,
        )
    ).scalar_one_or_none()

    if not gap:
        logger.warning(
            "Gap not found in project",
            gap_slug=gap_slug,
            project_id=str(project.id),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gap with slug '{gap_slug}' not found in this project",
        )

    return gap


@router.get(
    "/{organization_slug}/{project_slug}/gaps/metrics",
    response_model=dict,
)
def get_project_gaps_metrics(
    organization_slug: str,
    project_slug: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> dict:
    """Get gap metrics for a specific project."""
    logger.info(
        "Getting gap metrics for project",
        organization_slug=organization_slug,
        project_slug=project_slug,
        user_id=str(current_user.id),
    )

    # Get project (validates access)
    project = get_project_by_slugs(session, organization_slug, project_slug, current_user)

    # Calculate metrics scoped to project
    total_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id)
    ).scalar() or 0

    pending_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.status == "pending")
    ).scalar() or 0

    responded_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.status == "responded")
    ).scalar() or 0

    critical_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.priority == "critical")
    ).scalar() or 0

    high_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.priority == "high")
    ).scalar() or 0

    return {
        "total": total_gaps,
        "pending": pending_gaps,
        "responded": responded_gaps,
        "by_priority": {
            "critical": critical_gaps,
            "high": high_gaps,
            "medium": session.execute(
                select(func.count(Gap.id))
                .join(Document, Gap.document_id == Document.id)
                .where(Document.project_id == project.id, Gap.priority == "medium")
            ).scalar() or 0,
            "low": session.execute(
                select(func.count(Gap.id))
                .join(Document, Gap.document_id == Document.id)
                .where(Document.project_id == project.id, Gap.priority == "low")
            ).scalar() or 0,
        },
    }
