"""Integration tests for metrics API endpoint."""

from sqlalchemy.orm import Session

from shared.db.models import Gap, Proposal
from tests.fixtures import create_test_context


def test_get_metrics_authenticated(authenticated_client):
    """Test getting dashboard metrics with authentication."""
    response = authenticated_client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()

    # Verify structure
    assert "documents" in data
    assert "gaps" in data
    assert "proposals" in data
    assert "progress" in data

    # Verify document stats structure
    assert "total" in data["documents"]
    assert "avg_rating" in data["documents"]
    assert "healthy" in data["documents"]
    assert "needs_improvement" in data["documents"]
    assert "no_rating" in data["documents"]

    # Verify gap stats structure
    assert "total" in data["gaps"]
    assert "by_priority" in data["gaps"]
    assert "by_status" in data["gaps"]
    assert "pending" in data["gaps"]
    assert "critical" in data["gaps"]["by_priority"]
    assert "high" in data["gaps"]["by_priority"]
    assert "medium" in data["gaps"]["by_priority"]
    assert "low" in data["gaps"]["by_priority"]
    assert "pending" in data["gaps"]["by_status"]
    assert "responded" in data["gaps"]["by_status"]
    assert "rejected" in data["gaps"]["by_status"]

    # Verify proposal stats structure
    assert "total" in data["proposals"]
    assert "by_status" in data["proposals"]
    assert "pending" in data["proposals"]
    assert "pending" in data["proposals"]["by_status"]
    assert "accepted" in data["proposals"]["by_status"]
    assert "rejected" in data["proposals"]["by_status"]
    assert "implemented" in data["proposals"]["by_status"]

    # Verify progress metrics structure
    assert "gaps_resolved_percentage" in data["progress"]
    assert "documents_healthy_percentage" in data["progress"]
    assert "avg_resolution_time_hours" in data["progress"]
    assert "proposal_acceptance_rate" in data["progress"]

    # Verify data types
    assert isinstance(data["documents"]["total"], int)
    assert isinstance(data["gaps"]["total"], int)
    assert isinstance(data["proposals"]["total"], int)
    assert isinstance(data["progress"]["gaps_resolved_percentage"], int)
    assert isinstance(data["progress"]["documents_healthy_percentage"], int)
    assert isinstance(data["progress"]["proposal_acceptance_rate"], int)


def test_get_metrics_with_data(db_session: Session, authenticated_client):
    """Test getting metrics with documents, gaps, and proposals in database."""
    # Create test data
    user, org, project, document = create_test_context(db_session)

    # Add rating to document
    document.rating = 8.5
    db_session.commit()

    # Create a gap
    gap = Gap(
        document_id=document.id,
        slug="test-gap",
        question="Test question?",
        context_missing="Test context",
        priority="high",
        status="pending",
    )
    db_session.add(gap)
    db_session.commit()

    # Create a proposal
    proposal = Proposal(
        name="Test Proposal",
        slug="test-proposal",
        description="Test description",
        status="pending",
    )
    db_session.add(proposal)
    db_session.commit()

    # Get metrics
    response = authenticated_client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()

    # Verify counts reflect the data we created
    assert data["documents"]["total"] >= 1
    assert data["gaps"]["total"] >= 1
    assert data["proposals"]["total"] >= 1
