"""Project API endpoints for CRUD operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Organization, Project, User
from shared.db.session import get_db_dependency
from shared.schemas.project import ProjectCreate, ProjectListItem, ProjectResponse
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
) -> list[Project]:
    """
    List projects for the current user.

    Returns all projects in organizations where the user is the creator.
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

    logger.info(
        "Projects listed",
        count=len(projects),
    )

    return projects


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
