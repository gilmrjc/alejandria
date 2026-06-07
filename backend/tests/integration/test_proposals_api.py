"""Integration tests for proposals API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from shared.db.models import Proposal, User
from shared.db.session import get_db_session


@pytest.mark.asyncio
async def test_create_proposal(async_client: AsyncClient, test_user: User):
    """Test creating a new proposal."""
    response = await async_client.post(
        "/api/v1/proposals",
        json={
            "name": "Update documentation",
            "description": "Add missing sections to the documentation",
        },
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Update documentation"
    assert data["description"] == "Add missing sections to the documentation"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_list_proposals(
    async_client: AsyncClient, test_user: User, test_proposal: Proposal
):
    """Test listing proposals."""
    response = await async_client.get(
        "/api/v1/proposals",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_proposal(
    async_client: AsyncClient, test_user: User, test_proposal: Proposal
):
    """Test getting a specific proposal."""
    response = await async_client.get(
        f"/api/v1/proposals/{test_proposal.id}",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_proposal.id)
    assert data["name"] == test_proposal.name


@pytest.mark.asyncio
async def test_update_proposal(
    async_client: AsyncClient, test_user: User, test_proposal: Proposal
):
    """Test updating a proposal."""
    response = await async_client.put(
        f"/api/v1/proposals/{test_proposal.id}",
        json={"status": "accepted"},
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"


@pytest.mark.asyncio
async def test_delete_proposal(
    async_client: AsyncClient, test_user: User, test_proposal: Proposal
):
    """Test deleting a proposal."""
    response = await async_client.delete(
        f"/api/v1/proposals/{test_proposal.id}",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 204

    # Verify proposal is deleted
    async with get_db_session() as session:
        proposal = session.execute(
            select(Proposal).where(Proposal.id == test_proposal.id)
        ).scalar_one_or_none()
        assert proposal is None


@pytest.mark.asyncio
async def test_filter_proposals_by_status(
    async_client: AsyncClient, test_user: User, test_proposal: Proposal
):
    """Test filtering proposals by status."""
    response = await async_client.get(
        "/api/v1/proposals?status=pending",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    for proposal in data["items"]:
        assert proposal["status"] == "pending"
