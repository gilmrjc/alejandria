"""Dashboard metrics schemas for API response validation."""

from pydantic import BaseModel, Field


class DocumentStats(BaseModel):
    """Document statistics."""

    total: int = Field(description="Total number of documents")
    avgRating: float | None = Field(None, description="Average document rating")
    healthy: int = Field(description="Number of documents with rating >= 9")
    needsImprovement: int = Field(description="Number of documents with rating < 9")
    noRating: int = Field(description="Number of documents without rating")


class GapByPriority(BaseModel):
    """Gap counts by priority."""

    critical: int = Field(description="Number of critical gaps")
    high: int = Field(description="Number of high priority gaps")
    medium: int = Field(description="Number of medium priority gaps")
    low: int = Field(description="Number of low priority gaps")


class GapByStatus(BaseModel):
    """Gap counts by status."""

    pending: int = Field(description="Number of pending gaps")
    responded: int = Field(description="Number of responded gaps")
    rejected: int = Field(description="Number of rejected gaps")


class GapStats(BaseModel):
    """Gap statistics."""

    total: int = Field(description="Total number of gaps")
    byPriority: GapByPriority = Field(description="Gap counts by priority")
    byStatus: GapByStatus = Field(description="Gap counts by status")
    pending: int = Field(description="Number of pending gaps")


class ProposalByStatus(BaseModel):
    """Proposal counts by status."""

    pending: int = Field(description="Number of pending proposals")
    accepted: int = Field(description="Number of accepted proposals")
    rejected: int = Field(description="Number of rejected proposals")
    implemented: int = Field(description="Number of implemented proposals")


class ProposalStats(BaseModel):
    """Proposal statistics."""

    total: int = Field(description="Total number of proposals")
    byStatus: ProposalByStatus = Field(description="Proposal counts by status")
    pending: int = Field(description="Number of pending proposals")


class ProgressMetrics(BaseModel):
    """Progress metrics."""

    gapsResolvedPercentage: int = Field(
        description="Percentage of gaps resolved"
    )
    documentsHealthyPercentage: int = Field(
        description="Percentage of healthy documents"
    )
    avgResolutionTimeHours: float | None = Field(
        None, description="Average time to resolve gaps in hours"
    )
    proposalAcceptanceRate: int = Field(
        description="Percentage of proposals implemented"
    )


class DashboardMetricsResponse(BaseModel):
    """Dashboard metrics response."""

    documents: DocumentStats = Field(description="Document statistics")
    gaps: GapStats = Field(description="Gap statistics")
    proposals: ProposalStats = Field(description="Proposal statistics")
    progress: ProgressMetrics = Field(description="Progress metrics")
