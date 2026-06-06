"""Organization schemas for API request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class OrganizationBase(BaseModel):
    """Base organization schema with common fields."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="Organization name"
    )
    slug: str = Field(..., min_length=1, max_length=50, description="URL-safe slug")


class OrganizationCreate(OrganizationBase):
    """Schema for creating an organization."""

    is_personal: bool = Field(
        default=False, description="Whether this is a personal organization"
    )


class OrganizationResponse(BaseModel):
    """Schema for organization response."""

    id: UUID = Field(description="Organization ID")
    name: str = Field(description="Organization name")
    slug: str = Field(description="URL-safe slug")
    is_personal: bool = Field(description="Whether this is a personal organization")
    created_by: UUID = Field(description="Creator user ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    model_config = {"from_attributes": True}


class OrganizationListItem(BaseModel):
    """Schema for organization list item."""

    id: UUID = Field(description="Organization ID")
    name: str = Field(description="Organization name")
    slug: str = Field(description="URL-safe slug")
    is_personal: bool = Field(description="Whether this is a personal organization")
    created_at: datetime = Field(description="Creation timestamp")

    model_config = {"from_attributes": True}
