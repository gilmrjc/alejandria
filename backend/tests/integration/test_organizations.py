"""Integration tests for organization endpoints."""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.main import app
from shared.auth.jwt import get_password_hash
from shared.db.models import Organization, User
from shared.db.session import get_db_session


def test_create_organization_success(db_session: Session):
    """Test successful organization creation."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create user
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login to get token
    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        # Create organization
        response = client.post(
            "/api/v1/organizations",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Test Org",
                "slug": "test-org",
                "is_personal": False,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Org"
        assert data["slug"] == "test-org"
        assert data["is_personal"] is False
        assert data["created_by"] == str(user.id)

        # Verify in database
        org = db_session.execute(
            select(Organization).where(Organization.slug == "test-org")
        ).scalar_one_or_none()
        assert org is not None
        assert org.name == "Test Org"

    app.dependency_overrides.clear()


def test_create_organization_duplicate_slug(db_session: Session):
    """Test organization creation with duplicate slug fails."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create user
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create existing organization
    org = Organization(
        name="Existing Org",
        slug="test-org",
        is_personal=False,
        created_by=user.id,
    )
    db_session.add(org)
    db_session.commit()

    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/organizations",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "New Org",
                "slug": "test-org",
                "is_personal": False,
            },
        )

        assert response.status_code == 409
        assert "Slug already taken" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_list_organizations(db_session: Session):
    """Test listing organizations for current user."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create user
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create organizations
    org1 = Organization(
        name="Org 1",
        slug="org-1",
        is_personal=False,
        created_by=user.id,
    )
    org2 = Organization(
        name="Org 2",
        slug="org-2",
        is_personal=False,
        created_by=user.id,
    )
    db_session.add_all([org1, org2])
    db_session.commit()

    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/organizations",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(org["slug"] == "org-1" for org in data)
        assert any(org["slug"] == "org-2" for org in data)

    app.dependency_overrides.clear()


def test_get_organization(db_session: Session):
    """Test getting a specific organization."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create user
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create organization
    org = Organization(
        name="Test Org",
        slug="test-org",
        is_personal=False,
        created_by=user.id,
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/organizations/{org.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(org.id)
        assert data["name"] == "Test Org"
        assert data["slug"] == "test-org"

    app.dependency_overrides.clear()


def test_get_organization_not_found(db_session: Session):
    """Test getting non-existent organization."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create user
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        fake_id = uuid.uuid4()
        response = client.get(
            f"/api/v1/organizations/{fake_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_get_organization_access_denied(db_session: Session):
    """Test getting organization created by another user."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create two users
    user1 = User(
        email="user1@example.com",
        username="user1",
        password_hash=get_password_hash("password123"),
        is_active=True,
    )
    user2 = User(
        email="user2@example.com",
        username="user2",
        password_hash=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add_all([user1, user2])
    db_session.commit()
    db_session.refresh(user1)
    db_session.refresh(user2)

    # Create organization for user1
    org = Organization(
        name="User1 Org",
        slug="user1-org",
        is_personal=False,
        created_by=user1.id,
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    with TestClient(app) as client:
        # Login as user2
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "user2@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        # Try to access user1's organization
        response = client.get(
            f"/api/v1/organizations/{org.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    app.dependency_overrides.clear()
