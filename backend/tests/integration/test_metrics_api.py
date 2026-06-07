"""Integration tests for metrics API endpoint."""

import pytest
from sqlalchemy.orm import Session

from shared.db.models import Document, Gap, Proposal
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
    assert "avgRating" in data["documents"]
    assert "healthy" in data["documents"]
    assert "needsImprovement" in data["documents"]
    assert "noRating" in data["documents"]

    # Verify gap stats structure
    assert "total" in data["gaps"]
    assert "byPriority" in data["gaps"]
    assert "byStatus" in data["gaps"]
    assert "pending" in data["gaps"]
    assert "critical" in data["gaps"]["byPriority"]
    assert "high" in data["gaps"]["byPriority"]
    assert "medium" in data["gaps"]["byPriority"]
    assert "low" in data["gaps"]["byPriority"]
    assert "pending" in data["gaps"]["byStatus"]
    assert "responded" in data["gaps"]["byStatus"]
    assert "rejected" in data["gaps"]["byStatus"]

    # Verify proposal stats structure
    assert "total" in data["proposals"]
    assert "byStatus" in data["proposals"]
    assert "pending" in data["proposals"]
    assert "pending" in data["proposals"]["byStatus"]
    assert "accepted" in data["proposals"]["byStatus"]
    assert "rejected" in data["proposals"]["byStatus"]
    assert "implemented" in data["proposals"]["byStatus"]

    # Verify progress metrics structure
    assert "gapsResolvedPercentage" in data["progress"]
    assert "documentsHealthyPercentage" in data["progress"]
    assert "avgResolutionTimeHours" in data["progress"]
    assert "proposalAcceptanceRate" in data["progress"]

    # Verify data types
    assert isinstance(data["documents"]["total"], int)
    assert isinstance(data["gaps"]["total"], int)
    assert isinstance(data["proposals"]["total"], int)
    assert isinstance(data["progress"]["gapsResolvedPercentage"], int)
    assert isinstance(data["progress"]["documentsHealthyPercentage"], int)
    assert isinstance(data["progress"]["proposalAcceptanceRate"], int)


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
