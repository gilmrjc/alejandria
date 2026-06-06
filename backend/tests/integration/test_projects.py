"""Integration tests for project endpoints."""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.main import app
from shared.auth.jwt import get_password_hash
from shared.db.models import Organization, Project, User
from shared.db.session import get_db_session


def test_create_project_success(db_session: Session):
    """Test successful project creation."""

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

        # Create project
        response = client.post(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Test Project",
                "slug": "test-project",
                "description": "A test project",
                "organization_id": str(org.id),
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Project"
        assert data["slug"] == "test-project"
        assert data["description"] == "A test project"
        assert data["organization_id"] == str(org.id)
        assert data["created_by"] == str(user.id)

        # Verify in database
        project = db_session.execute(
            select(Project).where(Project.slug == "test-project")
        ).scalar_one_or_none()
        assert project is not None
        assert project.name == "Test Project"

    app.dependency_overrides.clear()


def test_create_project_duplicate_slug(db_session: Session):
    """Test project creation with duplicate slug in organization fails."""

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

    # Create existing project
    project = Project(
        name="Existing Project",
        slug="test-project",
        description="Existing",
        organization_id=org.id,
        created_by=user.id,
    )
    db_session.add(project)
    db_session.commit()

    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "New Project",
                "slug": "test-project",
                "description": "New",
                "organization_id": str(org.id),
            },
        )

        assert response.status_code == 409
        assert "Slug already taken" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_create_project_organization_not_found(db_session: Session):
    """Test project creation with non-existent organization fails."""

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

        fake_org_id = uuid.uuid4()
        response = client.post(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Test Project",
                "slug": "test-project",
                "description": "A test project",
                "organization_id": str(fake_org_id),
            },
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_create_project_access_denied(db_session: Session):
    """Test project creation in organization not owned by user fails."""

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

        # Try to create project in user1's organization
        response = client.post(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Test Project",
                "slug": "test-project",
                "description": "A test project",
                "organization_id": str(org.id),
            },
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_list_projects(db_session: Session):
    """Test listing projects for current user."""

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

    # Create projects
    project1 = Project(
        name="Project 1",
        slug="project-1",
        description="First project",
        organization_id=org.id,
        created_by=user.id,
    )
    project2 = Project(
        name="Project 2",
        slug="project-2",
        description="Second project",
        organization_id=org.id,
        created_by=user.id,
    )
    db_session.add_all([project1, project2])
    db_session.commit()

    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(proj["slug"] == "project-1" for proj in data)
        assert any(proj["slug"] == "project-2" for proj in data)

    app.dependency_overrides.clear()


def test_get_project(db_session: Session):
    """Test getting a specific project."""

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

    # Create project
    project = Project(
        name="Test Project",
        slug="test-project",
        description="A test project",
        organization_id=org.id,
        created_by=user.id,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/projects/{project.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(project.id)
        assert data["name"] == "Test Project"
        assert data["slug"] == "test-project"

    app.dependency_overrides.clear()


def test_get_project_not_found(db_session: Session):
    """Test getting non-existent project."""

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
            f"/api/v1/projects/{fake_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_get_project_access_denied(db_session: Session):
    """Test getting project from organization not owned by user."""

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

    # Create project for user1
    project = Project(
        name="User1 Project",
        slug="user1-project",
        description="User1's project",
        organization_id=org.id,
        created_by=user1.id,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    with TestClient(app) as client:
        # Login as user2
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "user2@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        # Try to access user1's project
        response = client.get(
            f"/api/v1/projects/{project.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    app.dependency_overrides.clear()
