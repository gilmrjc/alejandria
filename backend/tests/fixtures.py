"""Test fixture factory to reduce duplication in test setup."""

import uuid

from sqlalchemy.orm import Session

from shared.auth.jwt import get_password_hash
from shared.db.models import Document, Organization, Project, User


def create_test_user(session: Session, email: str = None, username: str = None) -> User:
    """
    Create a test user in the database with personal organization.

    Args:
        session: Database session
        email: Optional email (generates unique if not provided)
        username: Optional username (generates unique if not provided)

    Returns:
        Created User instance
    """
    unique_id = str(uuid.uuid4())[:8]
    user = User(
        email=email or f"test{unique_id}@example.com",
        username=username or f"testuser{unique_id}",
        password_hash=get_password_hash("testpass123"),
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create personal organization automatically
    org = Organization(
        name=f"{user.username}'s Personal Space",
        slug=f"{user.username}-personal",
        is_personal=True,
        created_by=user.id,
    )
    session.add(org)
    session.commit()
    session.refresh(org)

    return user


def create_test_organization(
    session: Session, user: User, name: str = None
) -> Organization:
    """
    Create a test organization for a user.

    Args:
        session: Database session
        user: User who owns the organization
        name: Optional organization name (generates unique if not provided)

    Returns:
        Created Organization instance
    """
    unique_id = str(uuid.uuid4())[:8]
    org = Organization(
        name=name or f"Test Org {unique_id}",
        slug=f"test-org-{unique_id}",
        created_by=user.id,
    )
    session.add(org)
    session.commit()
    session.refresh(org)
    return org


def create_test_project(
    session: Session, organization: Organization, user: User, name: str = None
) -> Project:
    """
    Create a test project for an organization.

    Args:
        session: Database session
        organization: Organization the project belongs to
        user: User who created the project
        name: Optional project name (generates unique if not provided)

    Returns:
        Created Project instance
    """
    unique_id = str(uuid.uuid4())[:8]
    project = Project(
        name=name or f"Test Project {unique_id}",
        slug=f"test-project-{unique_id}",
        organization_id=organization.id,
        created_by=user.id,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def create_test_document(
    session: Session,
    project: Project,
    organization: Organization,
    user: User,
    title: str = None,
    content: str = None,
) -> Document:
    """
    Create a test document for a project.

    Args:
        session: Database session
        project: Project the document belongs to
        organization: Organization the document belongs to
        user: User who created the document
        title: Optional document title (generates unique if not provided)
        content: Optional document content

    Returns:
        Created Document instance
    """
    unique_id = str(uuid.uuid4())[:8]
    document = Document(
        title=title or f"Test Document {unique_id}",
        slug=f"test-document-{unique_id}",
        content=content or "# Test\n\nContent",
        filename="test.md",
        project_id=project.id,
        organization_id=organization.id,
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


def create_test_context(
    session: Session,
) -> tuple[User, Organization, Project, Document]:
    """
    Create a complete test context with user, org, project, and document.

    Args:
        session: Database session

    Returns:
        Tuple of (user, organization, project, document)
    """
    user = create_test_user(session)
    org = create_test_organization(session, user)
    project = create_test_project(session, org, user)
    document = create_test_document(session, project, org, user)
    return user, org, project, document
