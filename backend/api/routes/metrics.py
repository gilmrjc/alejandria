"""Dashboard metrics API endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from shared.auth.jwt import get_current_user
from shared.db.models import Document, Gap, Organization, Project, Proposal, User
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
from shared.utils.logging import get_logger

logger = get_logger(__name__)

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


@router.get("/{organization_slug}/{project_slug}", response_model=DashboardMetricsResponse)
def get_project_metrics(
    organization_slug: str,
    project_slug: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> DashboardMetricsResponse:
    """
    Get dashboard metrics for a specific project.

    Returns document, gap, and proposal statistics filtered by project.
    """
    logger.info(
        "Getting project metrics",
        organization_slug=organization_slug,
        project_slug=project_slug,
        user_id=str(current_user.id),
    )

    # Get organization
    org = session.execute(
        select(Organization).where(Organization.slug == organization_slug)
    ).scalar_one_or_none()

    if not org:
        logger.warning(
            "Organization not found for metrics",
            organization_slug=organization_slug,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization '{organization_slug}' not found",
        )

    # Verify user has access
    if org.created_by != current_user.id:
        logger.warning(
            "Access denied to organization metrics",
            organization_slug=organization_slug,
            user_id=str(current_user.id),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this organization",
        )

    # Get project
    project = session.execute(
        select(Project).where(
            Project.organization_id == org.id,
            Project.slug == project_slug,
        )
    ).scalar_one_or_none()

    if not project:
        logger.warning(
            "Project not found for metrics",
            organization_slug=organization_slug,
            project_slug=project_slug,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_slug}' not found in organization '{organization_slug}'",
        )

    # Debug: Check project ID
    logger.info(
        "Calculating metrics for project",
        project_id=str(project.id),
        project_slug=project_slug,
    )

    # Document stats scoped to project
    total_docs = session.execute(
        select(func.count(Document.id)).where(Document.project_id == project.id)
    ).scalar()
    avg_rating = session.execute(
        select(func.avg(Document.rating))
        .where(Document.project_id == project.id, Document.rating.isnot(None))
    ).scalar()
    healthy_docs = session.execute(
        select(func.count(Document.id))
        .where(Document.project_id == project.id, Document.rating >= 9)
    ).scalar()
    needs_improvement_docs = session.execute(
        select(func.count(Document.id))
        .where(
            Document.project_id == project.id,
            Document.rating.isnot(None),
            Document.rating < 9,
        )
    ).scalar()
    no_rating_docs = session.execute(
        select(func.count(Document.id))
        .where(Document.project_id == project.id, Document.rating.is_(None))
    ).scalar()

    logger.info(
        "Document stats calculated",
        project_id=str(project.id),
        total_docs=total_docs,
        healthy=healthy_docs,
        needs_improvement=needs_improvement_docs,
        no_rating=no_rating_docs,
    )

    document_stats = DocumentStats(
        total=total_docs or 0,
        avg_rating=round(avg_rating, 1) if avg_rating else None,
        healthy=healthy_docs or 0,
        needs_improvement=needs_improvement_docs or 0,
        no_rating=no_rating_docs or 0,
    )

    # Gap stats by priority scoped to project
    critical_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.priority == "critical")
    ).scalar()
    high_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.priority == "high")
    ).scalar()
    medium_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.priority == "medium")
    ).scalar()
    low_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.priority == "low")
    ).scalar()

    # Gap stats by status scoped to project
    pending_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.status == "pending")
    ).scalar()
    responded_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.status == "responded")
    ).scalar()
    rejected_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id, Gap.status == "rejected")
    ).scalar()

    total_gaps = session.execute(
        select(func.count(Gap.id))
        .join(Document, Gap.document_id == Document.id)
        .where(Document.project_id == project.id)
    ).scalar()

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

    # Proposal stats scoped to project
    # Note: Proposals are not directly linked to projects in current schema,
    # so we return 0 for now. This can be extended when proposals are linked.
    proposal_stats = ProposalStats(
        total=0,
        by_status=ProposalByStatus(
            pending=0,
            accepted=0,
            rejected=0,
            implemented=0,
        ),
        pending=0,
    )

    # Progress metrics scoped to project
    gaps_resolved_percentage = (
        round((responded_gaps / total_gaps) * 100) if total_gaps else 0
    )
    documents_healthy_percentage = (
        round((healthy_docs / total_docs) * 100) if total_docs else 0
    )

    progress_metrics = ProgressMetrics(
        gaps_resolved_percentage=gaps_resolved_percentage,
        documents_healthy_percentage=documents_healthy_percentage,
        avg_resolution_time_hours=None,  # Would need project-scoped resolution time
        proposal_acceptance_rate=0,
    )

    logger.info(
        "Project metrics calculated",
        organization_slug=organization_slug,
        project_slug=project_slug,
        total_docs=document_stats.total,
        total_gaps=gap_stats.total,
    )

    return DashboardMetricsResponse(
        documents=document_stats,
        gaps=gap_stats,
        proposals=proposal_stats,
        progress=progress_metrics,
    )
