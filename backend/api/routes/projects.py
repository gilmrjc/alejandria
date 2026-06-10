"""Project API endpoints for CRUD operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Document, Gap, Organization, Project, User
from shared.db.session import get_db_dependency
from shared.schemas.project import ProjectCreate, ProjectListItem, ProjectMetrics, ProjectResponse
from shared.utils.logging import get_logger

logger = get_logger(__name__)

SessionDep = Annotated[Session, Depends(get_db_dependency)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Project:
    """
    Create a new project.

    Side effects:
    - Creates project within organization
    - Validates slug uniqueness within organization
    - Validates user is creator of organization
    """
    logger.info(
        "Project creation attempt",
        user_id=str(current_user.id),
        name=project_data.name,
        slug=project_data.slug,
        organization_id=str(project_data.organization_id),
    )

    # Verify organization exists and user is creator
    org = session.execute(
        select(Organization).where(
            Organization.id == project_data.organization_id,
            Organization.created_by == current_user.id,
        )
    ).scalar_one_or_none()

    if not org:
        logger.warning(
            "Project creation failed: organization not found or access denied",
            organization_id=str(project_data.organization_id),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found or access denied",
        )

    # Check if slug already exists in this organization
    existing_slug = session.execute(
        select(Project).where(
            Project.organization_id == project_data.organization_id,
            Project.slug == project_data.slug,
        )
    ).scalar_one_or_none()

    if existing_slug:
        logger.warning(
            "Project creation failed: slug already exists in organization",
            slug=project_data.slug,
            organization_id=str(project_data.organization_id),
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slug already taken in this organization",
        )

    # Create project
    project = Project(
        name=project_data.name,
        slug=project_data.slug,
        description=project_data.description,
        organization_id=project_data.organization_id,
        created_by=current_user.id,
    )
    session.add(project)
    session.commit()
    session.refresh(project)

    logger.info(
        "Project created successfully",
        project_id=str(project.id),
        slug=project.slug,
    )

    return project


@router.get("", response_model=list[ProjectListItem])
def list_projects(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> list[ProjectListItem]:
    """
    List projects for the current user with summary metrics.

    Returns all projects in organizations where the user is the creator,
    including document count, gap count, and average rating.
    """
    logger.info(
        "Listing projects",
        user_id=str(current_user.id),
    )

    # Get user's organizations
    user_org_ids = (
        session.execute(
            select(Organization.id).where(Organization.created_by == current_user.id)
        )
        .scalars()
        .all()
    )

    # Get projects in those organizations
    projects = (
        session.execute(
            select(Project).where(Project.organization_id.in_(user_org_ids))
        )
        .scalars()
        .all()
    )

    # Build response with metrics per project
    result: list[ProjectListItem] = []
    for project in projects:
        # Document metrics
        doc_count = (
            session.execute(
                select(func.count(Document.id)).where(Document.project_id == project.id)
            ).scalar()
            or 0
        )
        avg_rating = session.execute(
            select(func.avg(Document.rating))
            .where(Document.project_id == project.id, Document.rating.isnot(None))
        ).scalar()
        healthy_count = (
            session.execute(
                select(func.count(Document.id))
                .where(Document.project_id == project.id, Document.rating >= 9)
            ).scalar()
            or 0
        )

        # Gap metrics
        gap_count = (
            session.execute(
                select(func.count(Gap.id))
                .join(Document, Gap.document_id == Document.id)
                .where(Document.project_id == project.id)
            ).scalar()
            or 0
        )
        pending_gap_count = (
            session.execute(
                select(func.count(Gap.id))
                .join(Document, Gap.document_id == Document.id)
                .where(Document.project_id == project.id, Gap.status == "pending")
            ).scalar()
            or 0
        )

        healthy_percentage = round((healthy_count / doc_count) * 100) if doc_count else 0

        metrics = ProjectMetrics(
            document_count=doc_count,
            gap_count=gap_count,
            pending_gap_count=pending_gap_count,
            avg_rating=round(avg_rating, 1) if avg_rating else None,
            healthy_percentage=healthy_percentage,
        )

        result.append(
            ProjectListItem(
                id=project.id,
                name=project.name,
                slug=project.slug,
                description=project.description,
                organization_id=project.organization_id,
                created_at=project.created_at,
                metrics=metrics,
            )
        )

    logger.info(
        "Projects listed",
        count=len(result),
    )

    return result


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Project:
    """
    Get a specific project by ID.

    Only returns projects in organizations where the user is the creator.
    """
    logger.info(
        "Getting project",
        project_id=project_id,
        user_id=str(current_user.id),
    )

    # Get user's organizations
    user_org_ids = (
        session.execute(
            select(Organization.id).where(Organization.created_by == current_user.id)
        )
        .scalars()
        .all()
    )

    # Get project
    project = session.execute(
        select(Project).where(
            Project.id == project_id,
            Project.organization_id.in_(user_org_ids),
        )
    ).scalar_one_or_none()

    if not project:
        logger.warning(
            "Project not found",
            project_id=project_id,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project
