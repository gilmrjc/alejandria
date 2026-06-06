"""Organization API endpoints for CRUD operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Organization, User
from shared.db.session import get_db_session
from shared.schemas.organization import (
    OrganizationCreate,
    OrganizationListItem,
    OrganizationResponse,
)
from shared.utils.logging import get_logger

logger = get_logger(__name__)

SessionDep = Annotated[Session, Depends(get_db_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post(
    "", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED
)
def create_organization(
    org_data: OrganizationCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Organization:
    """
    Create a new organization.

    Side effects:
    - Creates organization with creator
    - Validates slug uniqueness
    """
    logger.info(
        "Organization creation attempt",
        user_id=str(current_user.id),
        name=org_data.name,
        slug=org_data.slug,
    )

    # Check if slug already exists
    existing_slug = session.execute(
        select(Organization).where(Organization.slug == org_data.slug)
    ).scalar_one_or_none()

    if existing_slug:
        logger.warning(
            "Organization creation failed: slug already exists",
            slug=org_data.slug,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slug already taken",
        )

    # Create organization
    org = Organization(
        name=org_data.name,
        slug=org_data.slug,
        is_personal=org_data.is_personal,
        created_by=current_user.id,
    )
    session.add(org)
    session.commit()
    session.refresh(org)

    logger.info(
        "Organization created successfully",
        org_id=str(org.id),
        slug=org.slug,
    )

    return org


@router.get("", response_model=list[OrganizationListItem])
def list_organizations(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> list[Organization]:
    """
    List organizations for the current user.

    Returns all organizations where the user is the creator.
    """
    logger.info(
        "Listing organizations",
        user_id=str(current_user.id),
    )

    organizations = (
        session.execute(
            select(Organization).where(Organization.created_by == current_user.id)
        )
        .scalars()
        .all()
    )

    logger.info(
        "Organizations listed",
        count=len(organizations),
    )

    return organizations


@router.get("/{org_id}", response_model=OrganizationResponse)
def get_organization(
    org_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Organization:
    """
    Get a specific organization by ID.

    Only returns organizations where the user is the creator.
    """
    logger.info(
        "Getting organization",
        org_id=org_id,
        user_id=str(current_user.id),
    )

    org = session.execute(
        select(Organization).where(
            Organization.id == org_id,
            Organization.created_by == current_user.id,
        )
    ).scalar_one_or_none()

    if not org:
        logger.warning(
            "Organization not found",
            org_id=org_id,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return org
