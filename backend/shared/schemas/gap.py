"""Gap schemas for API request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class GapBase(BaseModel):
    """Base gap schema with common fields."""

    question: str = Field(..., min_length=1, description="Gap question")
    priority: str = Field(
        default="medium",
        pattern="^(critical|high|medium|low)$",
        description="Gap priority level",
    )
    context_missing: str | None = Field(None, description="Context that is missing")
    role_affected: str | None = Field(
        None, max_length=100, description="Role affected by this gap"
    )


class GapCreate(GapBase):
    """Schema for creating a gap."""

    document_id: UUID = Field(..., description="Document ID")


class GapUpdate(BaseModel):
    """Schema for updating a gap."""

    answer: str | None = Field(None, description="Answer to the gap question")
    status: str | None = Field(
        None, pattern="^(pending|responded|rejected)$", description="Gap status"
    )


class GapResponse(BaseModel):
    """Schema for gap response."""

    id: UUID = Field(description="Gap ID")
    document_id: UUID = Field(description="Document ID")
    question: str = Field(description="Gap question")
    priority: str = Field(description="Gap priority level")
    status: str = Field(description="Gap status")
    context_missing: str | None = Field(None, description="Context that is missing")
    role_affected: str | None = Field(None, description="Role affected by this gap")
    answer: str | None = Field(None, description="Answer to the gap question")
    answered_at: datetime | None = Field(
        None, description="Timestamp when gap was answered"
    )
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    model_config = {"from_attributes": True}


class GapListItem(BaseModel):
    """Schema for gap list item."""

    id: UUID = Field(description="Gap ID")
    document_id: UUID = Field(description="Document ID")
    question: str = Field(description="Gap question")
    priority: str = Field(description="Gap priority level")
    status: str = Field(description="Gap status")
    created_at: datetime = Field(description="Creation timestamp")

    model_config = {"from_attributes": True}


class GapListResponse(BaseModel):
    """Schema for paginated gap list response."""

    items: list[GapListItem] = Field(description="List of gaps")
    total: int = Field(description="Total number of gaps")
    page: int = Field(default=1, description="Current page number")
    per_page: int = Field(default=25, description="Items per page")
    total_pages: int = Field(description="Total number of pages")

    @field_validator("total_pages")
    @classmethod
    def calculate_total_pages(cls, v: int, info) -> int:
        """Calculate total pages from total and per_page."""
        total = info.data.get("total", 0)
        per_page = info.data.get("per_page", 25)
        return (total + per_page - 1) // per_page if per_page > 0 else 0
