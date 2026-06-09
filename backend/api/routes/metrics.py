"""Dashboard metrics API endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Document, Gap, Proposal, User
from shared.db.session import get_db_dependency
from shared.schemas.metrics import (
    DashboardMetricsResponse,
    DocumentStats,
    GapByPriority,
    GapByStatus,
    GapStats,
    ProgressMetrics,
    ProposalByStatus,
    ProposalStats,
)

SessionDep = Annotated[Session, Depends(get_db_dependency)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=DashboardMetricsResponse)
def get_dashboard_metrics(session: SessionDep) -> DashboardMetricsResponse:
    """
    Get dashboard metrics including document, gap, and proposal statistics.

    Calculates aggregated statistics directly from the database for efficiency.
    """
    # Document stats
    total_docs = session.execute(select(func.count(Document.id))).scalar()
    avg_rating = session.execute(
        select(func.avg(Document.rating)).where(Document.rating.isnot(None))
    ).scalar()
    healthy_docs = session.execute(
        select(func.count(Document.id)).where(Document.rating >= 9)
    ).scalar()
    needs_improvement_docs = session.execute(
        select(func.count(Document.id)).where(
            Document.rating.isnot(None), Document.rating < 9
        )
    ).scalar()
    no_rating_docs = session.execute(
        select(func.count(Document.id)).where(Document.rating.is_(None))
    ).scalar()

    document_stats = DocumentStats(
        total=total_docs or 0,
        avg_rating=round(avg_rating, 1) if avg_rating else None,
        healthy=healthy_docs or 0,
        needs_improvement=needs_improvement_docs or 0,
        no_rating=no_rating_docs or 0,
    )

    # Gap stats by priority
    critical_gaps = session.execute(
        select(func.count(Gap.id)).where(Gap.priority == "critical")
    ).scalar()
    high_gaps = session.execute(
        select(func.count(Gap.id)).where(Gap.priority == "high")
    ).scalar()
    medium_gaps = session.execute(
        select(func.count(Gap.id)).where(Gap.priority == "medium")
    ).scalar()
    low_gaps = session.execute(
        select(func.count(Gap.id)).where(Gap.priority == "low")
    ).scalar()

    # Gap stats by status
    pending_gaps = session.execute(
        select(func.count(Gap.id)).where(Gap.status == "pending")
    ).scalar()
    responded_gaps = session.execute(
        select(func.count(Gap.id)).where(Gap.status == "responded")
    ).scalar()
    rejected_gaps = session.execute(
        select(func.count(Gap.id)).where(Gap.status == "rejected")
    ).scalar()

    total_gaps = session.execute(select(func.count(Gap.id))).scalar()

    gap_stats = GapStats(
        total=total_gaps or 0,
        by_priority=GapByPriority(
            critical=critical_gaps or 0,
            high=high_gaps or 0,
            medium=medium_gaps or 0,
            low=low_gaps or 0,
        ),
        by_status=GapByStatus(
            pending=pending_gaps or 0,
            responded=responded_gaps or 0,
            rejected=rejected_gaps or 0,
        ),
        pending=pending_gaps or 0,
    )

    # Proposal stats by status
    pending_proposals = session.execute(
        select(func.count(Proposal.id)).where(Proposal.status == "pending")
    ).scalar()
    accepted_proposals = session.execute(
        select(func.count(Proposal.id)).where(Proposal.status == "accepted")
    ).scalar()
    rejected_proposals = session.execute(
        select(func.count(Proposal.id)).where(Proposal.status == "rejected")
    ).scalar()
    implemented_proposals = session.execute(
        select(func.count(Proposal.id)).where(Proposal.status == "implemented")
    ).scalar()

    total_proposals = session.execute(select(func.count(Proposal.id))).scalar()

    proposal_stats = ProposalStats(
        total=total_proposals or 0,
        by_status=ProposalByStatus(
            pending=pending_proposals or 0,
            accepted=accepted_proposals or 0,
            rejected=rejected_proposals or 0,
            implemented=implemented_proposals or 0,
        ),
        pending=pending_proposals or 0,
    )

    # Progress metrics
    gaps_resolved_percentage = (
        round((responded_gaps / total_gaps) * 100) if total_gaps else 0
    )
    documents_healthy_percentage = (
        round((healthy_docs / total_docs) * 100) if total_docs else 0
    )
    proposal_acceptance_rate = (
        round((implemented_proposals / total_proposals) * 100) if total_proposals else 0
    )

    # Average resolution time for gaps
    avg_resolution_time = session.execute(
        select(
            func.avg(func.extract("epoch", Gap.answered_at - Gap.created_at) / 3600)
        ).where(Gap.status == "responded", Gap.answered_at.isnot(None))
    ).scalar()

    progress_metrics = ProgressMetrics(
        gaps_resolved_percentage=gaps_resolved_percentage,
        documents_healthy_percentage=documents_healthy_percentage,
        avg_resolution_time_hours=round(avg_resolution_time, 1)
        if avg_resolution_time
        else None,
        proposal_acceptance_rate=proposal_acceptance_rate,
    )

    return DashboardMetricsResponse(
        documents=document_stats,
        gaps=gap_stats,
        proposals=proposal_stats,
        progress=progress_metrics,
    )
