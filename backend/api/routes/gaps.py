"""Gap API endpoints with CRUD operations."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Document, Gap, User
from shared.db.session import get_db_session
from shared.schemas.gap import (
    GapCreate,
    GapListItem,
    GapListResponse,
    GapResponse,
    GapUpdate,
)
from shared.utils.pagination import apply_pagination, build_pagination_response

SessionDep = Annotated[Session, Depends(get_db_session)]
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
) -> Gap:
    """Get a gap by slug."""
    gap = session.execute(select(Gap).where(Gap.slug == slug)).scalar_one_or_none()

    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gap not found"
        )

    return gap


@router.get("/{gap_id}", response_model=GapResponse)
def get_gap(
    gap_id: uuid.UUID,
    session: SessionDep,
) -> Gap:
    """Get a gap by ID."""
    gap = session.execute(select(Gap).where(Gap.id == gap_id)).scalar_one_or_none()

    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gap not found"
        )

    return gap


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

    # Convert to response format
    items = [
        GapListItem(
            id=gap.id,
            document_id=gap.document_id,
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
        gap.answered_at = None  # Will be set by database trigger or manually

    if gap_data.status is not None:
        gap.status = gap_data.status
        if gap_data.status == "responded" and gap.answer:
            from datetime import UTC, datetime

            gap.answered_at = datetime.now(UTC)

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
        gap.answered_at = None  # Will be set by database trigger or manually

    if gap_data.status is not None:
        gap.status = gap_data.status
        if gap_data.status == "responded" and gap.answer:
            from datetime import UTC, datetime

            gap.answered_at = datetime.now(UTC)

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
