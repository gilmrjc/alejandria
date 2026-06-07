"""Proposal API endpoints with CRUD operations."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Proposal, User
from shared.db.session import get_db_session
from shared.schemas.proposal import (
    ProposalCreate,
    ProposalListItem,
    ProposalListResponse,
    ProposalResponse,
    ProposalUpdate,
)
from shared.utils.pagination import apply_pagination, build_pagination_response

SessionDep = Annotated[Session, Depends(get_db_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/proposals", tags=["proposals"])


@router.post("", response_model=ProposalResponse, status_code=status.HTTP_201_CREATED)
def create_proposal(
    proposal_data: ProposalCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Proposal:
    """Create a new proposal."""
    # Generate slug from name
    slug = proposal_data.name.lower().replace(" ", "-")[:50]

    # Check if slug already exists
    existing = session.execute(
        select(Proposal).where(Proposal.slug == slug)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Proposal with slug '{slug}' already exists",
        )

    # Create proposal
    proposal = Proposal(
        slug=slug,
        name=proposal_data.name,
        description=proposal_data.description,
        status="pending",
    )

    session.add(proposal)
    session.commit()
    session.refresh(proposal)

    return proposal


@router.get("/{proposal_id}", response_model=ProposalResponse)
def get_proposal(
    proposal_id: uuid.UUID,
    session: SessionDep,
) -> Proposal:
    """Get a proposal by ID."""
    proposal = session.execute(
        select(Proposal).where(Proposal.id == proposal_id)
    ).scalar_one_or_none()

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found"
        )

    return proposal


@router.get("", response_model=ProposalListResponse)
def list_proposals(
    session: SessionDep,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    per_page: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 25,
    status: Annotated[str | None, Query(description="Filter by status")] = None,
) -> dict:
    """List proposals with pagination and filtering."""
    # Build query
    query = select(Proposal)

    # Apply filters
    if status is not None:
        query = query.where(Proposal.status == status)

    # Apply sorting (newest first)
    query = query.order_by(Proposal.created_at.desc())

    # Apply pagination
    proposals, total, total_pages = apply_pagination(
        query, session, page=page, per_page=per_page
    )

    # Convert to response format
    items = [
        ProposalListItem(
            id=proposal.id,
            slug=proposal.slug,
            name=proposal.name,
            status=proposal.status,
            created_at=proposal.created_at,
        )
        for proposal in proposals
    ]

    return build_pagination_response(items, page, per_page, total, total_pages)


@router.put("/{proposal_id}", response_model=ProposalResponse)
def update_proposal(
    proposal_id: uuid.UUID,
    proposal_data: ProposalUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Proposal:
    """Update a proposal (status)."""
    proposal = session.execute(
        select(Proposal).where(Proposal.id == proposal_id)
    ).scalar_one_or_none()

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found"
        )

    # Update status if provided
    if proposal_data.status is not None:
        proposal.status = proposal_data.status

    session.commit()
    session.refresh(proposal)

    return proposal


@router.delete("/{proposal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_proposal(
    proposal_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> None:
    """Delete a proposal."""
    proposal = session.execute(
        select(Proposal).where(Proposal.id == proposal_id)
    ).scalar_one_or_none()

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found"
        )

    session.delete(proposal)
    session.commit()
