"""Integration tests for gaps dashboard endpoint."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_get_gap_dashboard_empty(client: TestClient):
    """Test dashboard endpoint with no gaps."""
    response = client.get("/api/v1/gaps/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "theme_clusters" in data
    assert data["metrics"]["total_gaps"] == 0


@pytest.mark.integration
def test_get_gap_dashboard_with_filters(client: TestClient):
    """Test dashboard endpoint with status filter."""
    response = client.get("/api/v1/gaps/dashboard?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
