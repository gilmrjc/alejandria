"""Common schemas used across the API."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""

    page: int = Field(default=1, ge=1, description="Page number (starting from 1)")
    per_page: int = Field(
        default=25, ge=1, le=100, description="Items per page (max 100)"
    )
    sort_by: str | None = Field(default="updated_at", description="Field to sort by")
    order: str = Field(default="desc", pattern="^(asc|desc)$", description="Sort order")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""

    page: int = Field(description="Current page number")
    per_page: int = Field(description="Items per page")
    total: int = Field(description="Total number of items")
    total_pages: int = Field(description="Total number of pages")

    @field_validator("total_pages")
    @classmethod
    def calculate_total_pages(cls, v: int, info) -> int:
        """Calculate total pages from total and per_page."""
        if "per_page" in info.data and "total" in info.data:
            per_page = info.data["per_page"]
            total = info.data["total"]
            return (total + per_page - 1) // per_page if per_page > 0 else 0
        return v


class ServiceStatus(BaseModel):
    """Status of a single service."""

    status: str = Field(description="Service status: healthy, unhealthy, or unknown")
    message: str | None = Field(default=None, description="Additional status message")


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str = Field(description="Overall system status")
    timestamp: datetime = Field(description="ISO 8601 timestamp of health check")
    services: dict[str, ServiceStatus] = Field(
        description="Status of individual services"
    )
