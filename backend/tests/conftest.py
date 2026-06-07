"""Pytest configuration and fixtures for Alejandria tests."""

import os

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.main import app
from shared.auth.jwt import create_access_token, get_password_hash
from shared.db.models import Document, Gap, Organization, Project, Proposal, User
from shared.db.session import get_db_session


def run_migrations(database_url: str):
    """Run alembic migrations for the test database."""
    from alembic import command

    # Configure alembic to use the test database
    alembic_dir = os.path.join(os.path.dirname(__file__), "..", "alembic")
    config = Config()
    config.set_main_option("script_location", alembic_dir)
    config.set_main_option("sqlalchemy.url", database_url)

    # Run migrations
    command.upgrade(config, "head")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Automatically run alembic migrations before test session starts.

    This fixture runs automatically (autouse=True) to ensure the test database
    schema is up to date before any tests run.
    """
    # Build test database URL from environment variables
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_test_db = os.getenv("POSTGRES_TEST_DB")
    postgres_host = os.getenv("POSTGRES_HOST", "postgresql")

    if not all([postgres_user, postgres_password, postgres_test_db]):
        raise ValueError(
            "POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_TEST_DB "
            "must be set in environment"
        )

    database_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:5432/{postgres_test_db}"

    # Override DATABASE_URL for alembic
    original_db_url = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = database_url

    try:
        run_migrations(database_url)
    finally:
        # Restore original DATABASE_URL if it existed
        if original_db_url is not None:
            os.environ["DATABASE_URL"] = original_db_url
        elif "DATABASE_URL" in os.environ:
            del os.environ["DATABASE_URL"]

    yield


@pytest.fixture(scope="session")
def db_engine():
    """
    Session-scoped fixture to create database engine for tests.

    This uses the test database which is already migrated by setup_test_database.
    Tables are created by alembic migrations, not by SQLAlchemy metadata.
    """
    # Build test database URL from environment variables
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_test_db = os.getenv("POSTGRES_TEST_DB")
    postgres_host = os.getenv("POSTGRES_HOST", "postgresql")

    if not all([postgres_user, postgres_password, postgres_test_db]):
        raise ValueError(
            "POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_TEST_DB "
            "must be set in environment"
        )

    database_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:5432/{postgres_test_db}"

    # Create engine with connection pool settings for tests
    engine = create_engine(
        database_url,
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5},
    )

    yield engine

    # Cleanup: dispose engine after all tests
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Function-scoped fixture to provide a database session with transaction rollback.

    Each test gets a fresh session with transaction rollback for isolation.
    """
    # Create session with transaction for rollback
    connection = db_engine.connect()
    transaction = connection.begin()
    session_local = sessionmaker(bind=connection, autocommit=False, autoflush=False)
    session = session_local()

    yield session

    # Cleanup: rollback transaction
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def authenticated_client(db_session: Session):
    """
    Fixture to provide a TestClient with database session override and
    authenticated user.

    This creates a user, organization, and project, then returns a client
    with JWT token authentication.
    """
    from shared.auth.jwt import get_password_hash
    from shared.db.models import Organization, Project, User

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create test user
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
    org = Organization(name="Test Org", slug="test-org", created_by=user.id)
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    # Create project
    project = Project(
        name="Test Project",
        slug="test-project",
        organization_id=org.id,
        created_by=user.id,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    with TestClient(app) as test_client:
        # Login to get token
        login_response = test_client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        # Set default headers for authentication
        test_client.headers.update({"Authorization": f"Bearer {token}"})
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    Fixture to provide a TestClient with database session override.

    This ensures all API calls use the test database session.
    """

    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_settings(monkeypatch):
    """
    Fixture to mock settings for testing.

    This allows tests to override configuration values without
    affecting the actual settings module.
    """

    def _set_setting(key: str, value):
        monkeypatch.setattr(
            "shared.config.settings.settings",
            key,
            value,
        )

    return _set_setting


@pytest.fixture
def password_hash():
    """
    Fixture to provide a bcrypt password hash for testing.

    Returns a hash for "testpass123" to avoid bcrypt compatibility issues.
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash("testpass123")


@pytest.fixture(scope="function")
async def async_client(db_session: Session):
    """
    Fixture to provide an AsyncClient for async HTTP testing.

    This creates an async test client with database session override.
    """
    import httpx

    # Override database session
    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session: Session) -> User:
    """
    Fixture to create a test user with access token.

    Returns a User instance with access_token attribute set.
    """
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Add access_token attribute for authentication
    user.access_token = create_access_token(user_id=str(user.id), email=user.email)

    return user


@pytest.fixture(scope="function")
def test_organization(db_session: Session, test_user: User) -> Organization:
    """
    Fixture to create a test organization.
    """
    org = Organization(
        name="Test Org",
        slug="test-org",
        is_personal=False,
        created_by=test_user.id,
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)
    return org


@pytest.fixture(scope="function")
def test_project(
    db_session: Session, test_organization: Organization, test_user: User
) -> Project:
    """
    Fixture to create a test project.
    """
    project = Project(
        name="Test Project",
        slug="test-project",
        organization_id=test_organization.id,
        created_by=test_user.id,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


@pytest.fixture(scope="function")
def test_document(
    db_session: Session,
    test_project: Project,
    test_organization: Organization,
    test_user: User,
) -> Document:
    """
    Fixture to create a test document.
    """
    document = Document(
        project_id=test_project.id,
        organization_id=test_organization.id,
        title="Test Document",
        slug="test-document",
        content="This is a test document content.",
        filename="test.md",
        created_by=test_user.id,
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)
    return document


@pytest.fixture(scope="function")
def test_gap(db_session: Session, test_document: Document) -> Gap:
    """
    Fixture to create a test gap.
    """
    gap = Gap(
        document_id=test_document.id,
        slug="test-gap",
        question="What is the purpose of this document?",
        context_missing="Purpose statement",
        priority="high",
        status="pending",
    )
    db_session.add(gap)
    db_session.commit()
    db_session.refresh(gap)
    return gap


@pytest.fixture(scope="function")
def test_proposal(db_session: Session) -> Proposal:
    """
    Fixture to create a test proposal.
    """
    proposal = Proposal(
        slug="test-proposal",
        name="Update documentation",
        description="Add missing sections to the documentation",
        status="pending",
    )
    db_session.add(proposal)
    db_session.commit()
    db_session.refresh(proposal)
    return proposal
