"""Proposal API endpoints with CRUD operations."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Document, Gap, Proposal, ProposalDocument, ProposalGap, User
from shared.db.session import get_db_dependency
from shared.schemas.proposal import (
    ProposalApprove,
    ProposalCreate,
    ProposalDocumentDetail,
    ProposalGapDetail,
    ProposalListItem,
    ProposalListResponse,
    ProposalReject,
    ProposalResponse,
    ProposalUpdate,
    ProposalViewResponse,
)
from shared.utils.pagination import apply_pagination

SessionDep = Annotated[Session, Depends(get_db_dependency)]
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

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    }


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


@router.put("/{proposal_id}/approve", response_model=ProposalResponse)
def approve_proposal(
    proposal_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Proposal:
    """Approve a proposal and enqueue application job."""
    proposal = session.execute(
        select(Proposal).where(Proposal.id == proposal_id)
    ).scalar_one_or_none()

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found"
        )

    # Validate proposal is in pending status
    if proposal.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Proposal must be in pending status to approve, current status: {proposal.status}",
        )

    # Update status to accepted
    proposal.status = "accepted"
    session.commit()
    session.refresh(proposal)

    # Enqueue proposal_application task
    try:
        from jobs.tasks.proposal_application import proposal_application_task

        proposal_application_task.delay(str(proposal_id))
    except Exception as e:
        # Log warning but don't fail the request
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"Could not enqueue proposal_application for proposal {proposal_id}: {e}")

    return proposal


@router.put("/{proposal_id}/reject", response_model=ProposalResponse)
def reject_proposal(
    proposal_id: uuid.UUID,
    rejection_data: ProposalReject,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> Proposal:
    """Reject a proposal."""
    proposal = session.execute(
        select(Proposal).where(Proposal.id == proposal_id)
    ).scalar_one_or_none()

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found"
        )

    # Validate proposal is in pending status
    if proposal.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Proposal must be in pending status to reject, current status: {proposal.status}",
        )

    # Update status to rejected
    proposal.status = "rejected"

    # Append rejection reason to description if provided
    if rejection_data.reason:
        proposal.description = f"{proposal.description}\n\nRejection reason: {rejection_data.reason}"

    session.commit()
    session.refresh(proposal)

    return proposal


@router.get("/{proposal_id}/view", response_model=ProposalViewResponse)
def view_proposal(
    proposal_id: uuid.UUID,
    session: SessionDep,
) -> dict:
    """Get proposal with full details including related documents and gaps."""
    # Get proposal
    proposal = session.execute(
        select(Proposal).where(Proposal.id == proposal_id)
    ).scalar_one_or_none()

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found"
        )

    # Get related documents
    proposal_documents = session.execute(
        select(ProposalDocument).where(ProposalDocument.proposal_id == proposal_id)
    ).scalars().all()

    document_ids = [pd.document_id for pd in proposal_documents]
    documents = []
    if document_ids:
        docs = session.execute(
            select(Document).where(Document.id.in_(document_ids))
        ).scalars().all()
        documents = [
            ProposalDocumentDetail(
                id=doc.id,
                slug=doc.slug,
                title=doc.title,
                rating=doc.rating,
            )
            for doc in docs
        ]

    # Get related gaps
    proposal_gaps = session.execute(
        select(ProposalGap).where(ProposalGap.proposal_id == proposal_id)
    ).scalars().all()

    gap_ids = [pg.gap_id for pg in proposal_gaps]
    gaps = []
    if gap_ids:
        gap_records = session.execute(
            select(Gap).where(Gap.id.in_(gap_ids))
        ).scalars().all()
        gaps = [
            ProposalGapDetail(
                id=gap.id,
                slug=gap.slug,
                question=gap.question,
                answer=gap.answer,
                priority=gap.priority,
                status=gap.status,
                context_missing=gap.context_missing,
                role_affected=gap.role_affected,
            )
            for gap in gap_records
        ]

    return {
        "id": proposal.id,
        "slug": proposal.slug,
        "name": proposal.name,
        "description": proposal.description,
        "status": proposal.status,
        "created_at": proposal.created_at,
        "updated_at": proposal.updated_at,
        "documents": documents,
        "gaps": gaps,
    }
