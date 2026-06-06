"""Integration tests for database operations."""

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.db.models import Document, User
from shared.db.session import get_engine, get_session_maker


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to provide a database session using docker-compose test PostgreSQL.

    This uses the same PostgreSQL service but with a separate test database.
    Uses transaction rollback for test isolation.
    """
    from alembic.config import Config

    from alembic import command
    from shared.config.settings import settings

    # Create engine with test database URL (same host, different database)
    test_db_url = settings.test_database_url or settings.database_url
    test_db_url = test_db_url.replace("localhost", "postgresql")
    engine = get_engine(test_db_url)

    # Apply Alembic migrations to test database
    alembic_cfg = Config("/workspace/alembic.ini")
    # Set database URL for alembic
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    command.upgrade(alembic_cfg, "head")

    # Create session with autocommit=False, autoflush=False
    session_local = get_session_maker(engine)
    session = session_local()

    yield session

    # Cleanup: rollback transaction
    session.rollback()
    session.close()
    # Don't drop tables - they're shared with development


def test_create_document(db_session: Session, password_hash: str):
    """Test creating a document in the database."""
    import uuid

    from shared.db.models import Organization, Project

    # Create user first
    unique_id = str(uuid.uuid4())[:8]
    user = User(
        email=f"test{unique_id}@example.com",
        username=f"testuser{unique_id}",
        password_hash=password_hash,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create organization
    org = Organization(
        name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    # Create project
    project = Project(
        name="Test Project",
        slug=f"test-project-{unique_id}",
        organization_id=org.id,
        created_by=user.id,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    # Create document
    document = Document(
        title="Test Document",
        slug=f"test-document-{unique_id}",
        content="# Test\n\nContent",
        filename="test.md",
        project_id=project.id,
        organization_id=org.id,
    )

    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)

    assert document.id is not None
    assert document.title == "Test Document"
    assert document.slug == f"test-document-{unique_id}"


def test_read_document(db_session: Session, password_hash: str):
    """Test reading a document from the database."""
    import uuid

    from shared.db.models import Organization, Project

    # Create user first
    unique_id = str(uuid.uuid4())[:8]
    user = User(
        email=f"test{unique_id}@example.com",
        username=f"testuser{unique_id}",
        password_hash=password_hash,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create organization
    org = Organization(
        name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    # Create project
    project = Project(
        name="Test Project",
        slug=f"test-project-{unique_id}",
        organization_id=org.id,
        created_by=user.id,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    # Create document
    document = Document(
        title="Test Document",
        slug=f"test-document-{unique_id}",
        content="# Test\n\nContent",
        filename="test.md",
        project_id=project.id,
        organization_id=org.id,
    )

    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)

    # Read document
    retrieved = db_session.execute(
        select(Document).where(Document.id == document.id)
    ).scalar_one()

    assert retrieved.title == "Test Document"
    assert retrieved.content == "# Test\n\nContent"


def test_update_document(db_session: Session, password_hash: str):
    """Test updating a document in the database."""
    import uuid

    from shared.db.models import Organization, Project

    # Create user first
    unique_id = str(uuid.uuid4())[:8]
    user = User(
        email=f"test{unique_id}@example.com",
        username=f"testuser{unique_id}",
        password_hash=password_hash,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create organization
    org = Organization(
        name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    # Create project
    project = Project(
        name="Test Project",
        slug=f"test-project-{unique_id}",
        organization_id=org.id,
        created_by=user.id,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    # Create document
    document = Document(
        title="Test Document",
        slug=f"test-document-{unique_id}",
        content="# Test\n\nContent",
        filename="test.md",
        project_id=project.id,
        organization_id=org.id,
    )

    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)

    # Update document
    document.title = "Updated Document"
    document.content = "# Updated\n\nNew content"
    db_session.commit()
    db_session.refresh(document)

    assert document.title == "Updated Document"
    assert document.content == "# Updated\n\nNew content"


def test_delete_document(db_session: Session, password_hash: str):
    """Test deleting a document from the database."""
    import uuid

    from shared.db.models import Organization, Project

    # Create user first
    unique_id = str(uuid.uuid4())[:8]
    user = User(
        email=f"test{unique_id}@example.com",
        username=f"testuser{unique_id}",
        password_hash=password_hash,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create organization
    org = Organization(
        name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    # Create project
    project = Project(
        name="Test Project",
        slug=f"test-project-{unique_id}",
        organization_id=org.id,
        created_by=user.id,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    # Create document
    document = Document(
        title="Test Document",
        slug=f"test-document-{unique_id}",
        content="# Test\n\nContent",
        filename="test.md",
        project_id=project.id,
        organization_id=org.id,
    )

    db_session.add(document)
    db_session.commit()
    document_id = document.id

    # Delete document
    db_session.delete(document)
    db_session.commit()

    # Verify deletion
    retrieved = db_session.execute(
        select(Document).where(Document.id == document_id)
    ).scalar_one_or_none()

    assert retrieved is None


def test_create_user(db_session: Session, password_hash: str):
    """Test creating a user in the database."""
    # Use unique email to avoid conflicts with existing data
    import uuid

    unique_id = str(uuid.uuid4())[:8]

    user = User(
        email=f"test{unique_id}@example.com",
        username=f"testuser{unique_id}",
        password_hash=password_hash,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == f"test{unique_id}@example.com"
    assert user.username == f"testuser{unique_id}"
