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
        pattern="^(pending|accepted|rejected|implemented)$",
        description="Proposal status",
    )


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
