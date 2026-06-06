"""Integration tests for user registration endpoint."""

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.main import app
from shared.db.models import Organization, User
from shared.db.session import get_db_session


def test_register_user_success(db_session: Session):
    """Test successful user registration."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "password123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert data["is_active"] is True
        assert "id" in data

        # Verify user was created in database
        user = db_session.execute(
            select(User).where(User.email == "newuser@example.com")
        ).scalar_one_or_none()
        assert user is not None
        assert user.username == "newuser"

        # Verify personal organization was created
        org = db_session.execute(
            select(Organization).where(
                Organization.created_by == user.id, Organization.is_personal
            )
        ).scalar_one_or_none()
        assert org is not None
        assert org.slug == "newuser-personal"

    app.dependency_overrides.clear()


def test_register_user_duplicate_email(db_session: Session):
    """Test registration with duplicate email fails."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create existing user
    user = User(
        email="existing@example.com",
        username="existing",
        password_hash="hashed_password",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "existing@example.com",
                "username": "different",
                "password": "password123",
            },
        )

        assert response.status_code == 409
        assert "Email already registered" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_register_user_duplicate_username(db_session: Session):
    """Test registration with duplicate username fails."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create existing user
    user = User(
        email="existing@example.com",
        username="existing",
        password_hash="hashed_password",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "different@example.com",
                "username": "existing",
                "password": "password123",
            },
        )

        assert response.status_code == 409
        assert "Username already taken" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_register_user_invalid_email(db_session: Session):
    """Test registration with invalid email fails."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "username": "newuser",
                "password": "password123",
            },
        )

        assert response.status_code == 422  # Validation error

    app.dependency_overrides.clear()


def test_register_user_short_password(db_session: Session):
    """Test registration with short password fails."""

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "short",
            },
        )

        assert response.status_code == 422  # Validation error

    app.dependency_overrides.clear()
