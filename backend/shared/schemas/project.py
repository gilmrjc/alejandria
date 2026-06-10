"""Project schemas for API request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    slug: str = Field(..., min_length=1, max_length=50, description="URL-safe slug")
    description: str | None = Field(None, description="Project description")


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""

    organization_id: UUID = Field(..., description="Organization ID")


class ProjectResponse(BaseModel):
    """Schema for project response."""

    id: UUID = Field(description="Project ID")
    name: str = Field(description="Project name")
    slug: str = Field(description="URL-safe slug")
    description: str | None = Field(description="Project description")
    organization_id: UUID = Field(description="Organization ID")
    created_by: UUID = Field(description="Creator user ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    model_config = {"from_attributes": True}


class ProjectMetrics(BaseModel):
    """Summary metrics for a project displayed in list views."""

    document_count: int = Field(default=0, description="Number of documents")
    gap_count: int = Field(default=0, description="Number of gaps")
    pending_gap_count: int = Field(default=0, description="Number of pending gaps")
    avg_rating: float | None = Field(None, description="Average document rating")
    healthy_percentage: int = Field(default=0, description="Percentage of healthy documents")


class ProjectListItem(BaseModel):
    """Schema for project list item."""

    id: UUID = Field(description="Project ID")
    name: str = Field(description="Project name")
    slug: str = Field(description="URL-safe slug")
    description: str | None = Field(description="Project description")
    organization_id: UUID = Field(description="Organization ID")
    created_at: datetime = Field(description="Creation timestamp")
    metrics: ProjectMetrics = Field(default_factory=ProjectMetrics, description="Project summary metrics")

    model_config = {"from_attributes": True}
