"""Dashboard metrics schemas for API response validation."""

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class DocumentStats(BaseModel):
    """Document statistics."""

    model_config = ConfigDict(
        populate_by_name=True,
        by_alias=True,
        alias_generator=to_camel,
    )

    total: int = Field(description="Total number of documents")
    avg_rating: float | None = Field(
        None, alias="avgRating", description="Average document rating"
    )
    healthy: int = Field(description="Number of documents with rating >= 9")
    needs_improvement: int = Field(
        alias="needsImprovement", description="Number of documents with rating < 9"
    )
    no_rating: int = Field(
        alias="noRating", description="Number of documents without rating"
    )


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

    model_config = ConfigDict(
        populate_by_name=True,
        by_alias=True,
        alias_generator=to_camel,
    )

    total: int = Field(description="Total number of gaps")
    by_priority: GapByPriority = Field(
        alias="byPriority", description="Gap counts by priority"
    )
    by_status: GapByStatus = Field(
        alias="byStatus", description="Gap counts by status"
    )
    pending: int = Field(description="Number of pending gaps")


class ProposalByStatus(BaseModel):
    """Proposal counts by status."""

    pending: int = Field(description="Number of pending proposals")
    accepted: int = Field(description="Number of accepted proposals")
    rejected: int = Field(description="Number of rejected proposals")
    implemented: int = Field(description="Number of implemented proposals")


class ProposalStats(BaseModel):
    """Proposal statistics."""

    model_config = ConfigDict(
        populate_by_name=True,
        by_alias=True,
        alias_generator=to_camel,
    )

    total: int = Field(description="Total number of proposals")
    by_status: ProposalByStatus = Field(
        alias="byStatus", description="Proposal counts by status"
    )
    pending: int = Field(description="Number of pending proposals")


class ProgressMetrics(BaseModel):
    """Progress metrics."""

    model_config = ConfigDict(
        populate_by_name=True,
        by_alias=True,
        alias_generator=to_camel,
    )

    gaps_resolved_percentage: int = Field(
        alias="gapsResolvedPercentage", description="Percentage of gaps resolved"
    )
    documents_healthy_percentage: int = Field(
        alias="documentsHealthyPercentage",
        description="Percentage of healthy documents",
    )
    avg_resolution_time_hours: float | None = Field(
        None,
        alias="avgResolutionTimeHours",
        description="Average time to resolve gaps in hours",
    )
    proposal_acceptance_rate: int = Field(
        alias="proposalAcceptanceRate",
        description="Percentage of proposals implemented",
    )


class DashboardMetricsResponse(BaseModel):
    """Dashboard metrics response."""

    model_config = ConfigDict(
        populate_by_name=True,
        by_alias=True,
        alias_generator=to_camel,
    )

    documents: DocumentStats = Field(description="Document statistics")
    gaps: GapStats = Field(description="Gap statistics")
    proposals: ProposalStats = Field(description="Proposal statistics")
    progress: ProgressMetrics = Field(description="Progress metrics")
