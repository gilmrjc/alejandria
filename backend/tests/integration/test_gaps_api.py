"""Integration tests for gaps API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from shared.db.models import Document, Gap, User
from shared.db.session import get_db_session


@pytest.mark.asyncio
async def test_create_gap(
    async_client: AsyncClient, test_user: User, test_document: Document
):
    """Test creating a new gap."""
    response = await async_client.post(
        "/api/v1/gaps",
        json={
            "document_id": str(test_document.id),
            "question": "What is the purpose of this document?",
            "priority": "high",
            "context_missing": "Purpose statement",
        },
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == "What is the purpose of this document?"
    assert data["priority"] == "high"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_list_gaps(async_client: AsyncClient, test_user: User, test_gap: Gap):
    """Test listing gaps."""
    response = await async_client.get(
        "/api/v1/gaps",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_gap(async_client: AsyncClient, test_user: User, test_gap: Gap):
    """Test getting a specific gap."""
    response = await async_client.get(
        f"/api/v1/gaps/{test_gap.id}",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_gap.id)
    assert data["question"] == test_gap.question


@pytest.mark.asyncio
async def test_update_gap(async_client: AsyncClient, test_user: User, test_gap: Gap):
    """Test updating a gap."""
    response = await async_client.put(
        f"/api/v1/gaps/{test_gap.id}",
        json={
            "answer": "This document defines the system architecture.",
            "status": "responded",
        },
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This document defines the system architecture."
    assert data["status"] == "responded"


@pytest.mark.asyncio
async def test_delete_gap(async_client: AsyncClient, test_user: User, test_gap: Gap):
    """Test deleting a gap."""
    response = await async_client.delete(
        f"/api/v1/gaps/{test_gap.id}",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 204

    # Verify gap is deleted
    async with get_db_session() as session:
        gap = session.execute(
            select(Gap).where(Gap.id == test_gap.id)
        ).scalar_one_or_none()
        assert gap is None


@pytest.mark.asyncio
async def test_filter_gaps_by_status(
    async_client: AsyncClient, test_user: User, test_gap: Gap
):
    """Test filtering gaps by status."""
    response = await async_client.get(
        "/api/v1/gaps?status=pending",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    for gap in data["items"]:
        assert gap["status"] == "pending"


@pytest.mark.asyncio
async def test_filter_gaps_by_priority(
    async_client: AsyncClient, test_user: User, test_gap: Gap
):
    """Test filtering gaps by priority."""
    response = await async_client.get(
        "/api/v1/gaps?priority=high",
        headers={"Authorization": f"Bearer {test_user.access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    for gap in data["items"]:
        assert gap["priority"] == "high"
