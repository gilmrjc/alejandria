"""Proposal schemas for API request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProposalBase(BaseModel):
    """Base proposal schema with common fields."""

    name: str = Field(..., min_length=1, description="Proposal name")
    description: str = Field(..., min_length=1, description="Proposal description")


class ProposalCreate(ProposalBase):
    """Schema for creating a proposal."""

    # Additional fields can be added here as needed
    pass


class ProposalUpdate(BaseModel):
    """Schema for updating a proposal."""

    status: str | None = Field(
        None,
        pattern="^(pending|accepted|rejected|implemented|failed)$",
        description="Proposal status",
    )


class ProposalApprove(BaseModel):
    """Schema for approving a proposal."""

    pass


class ProposalReject(BaseModel):
    """Schema for rejecting a proposal."""

    reason: str | None = Field(None, description="Optional reason for rejection")


class ProposalResponse(BaseModel):
    """Schema for proposal response."""

    id: UUID = Field(description="Proposal ID")
    slug: str = Field(description="Proposal slug")
    name: str = Field(description="Proposal name")
    description: str = Field(description="Proposal description")
    status: str = Field(description="Proposal status")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    model_config = {"from_attributes": True}


class ProposalListItem(BaseModel):
    """Schema for proposal list item."""

    id: UUID = Field(description="Proposal ID")
    slug: str = Field(description="Proposal slug")
    name: str = Field(description="Proposal name")
    status: str = Field(description="Proposal status")
    created_at: datetime = Field(description="Creation timestamp")

    model_config = {"from_attributes": True}


class ProposalListResponse(BaseModel):
    """Schema for paginated proposal list response."""

    items: list[ProposalListItem] = Field(description="List of proposals")
    total: int = Field(description="Total number of proposals")
    page: int = Field(default=1, description="Current page number")
    per_page: int = Field(default=25, description="Items per page")
    total_pages: int = Field(description="Total number of pages")


class ProposalGapDetail(BaseModel):
    """Schema for gap details in proposal view."""

    id: UUID = Field(description="Gap ID")
    slug: str = Field(description="Gap slug")
    question: str = Field(description="Gap question")
    answer: str | None = Field(description="Gap answer")
    priority: str = Field(description="Gap priority")
    status: str = Field(description="Gap status")
    context_missing: str | None = Field(description="Missing context description")
    role_affected: str | None = Field(description="Role affected by gap")

    model_config = {"from_attributes": True}


class ProposalDocumentDetail(BaseModel):
    """Schema for document details in proposal view."""

    id: UUID = Field(description="Document ID")
    slug: str = Field(description="Document slug")
    title: str = Field(description="Document title")
    rating: float | None = Field(description="Document rating")

    model_config = {"from_attributes": True}


class ProposalViewResponse(BaseModel):
    """Schema for full proposal view with relationships."""

    id: UUID = Field(description="Proposal ID")
    slug: str = Field(description="Proposal slug")
    name: str = Field(description="Proposal name")
    description: str = Field(description="Proposal description/instructions")
    status: str = Field(description="Proposal status")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    documents: list[ProposalDocumentDetail] = Field(description="Related documents")
    gaps: list[ProposalGapDetail] = Field(description="Related gaps with details")

    model_config = {"from_attributes": True}
