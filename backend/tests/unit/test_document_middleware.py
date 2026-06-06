"""Unit tests for document versioning middleware."""

import uuid

import pytest

from shared.auth.jwt import get_password_hash
from shared.db.models import Document, DocumentSnapshot, Organization, Project, User


class TestDocumentVersioningMiddleware:
    """Test document versioning middleware behavior."""

    def setup_document_context(self, db_session):
        """Helper to set up user, org, project for document tests."""
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"test{unique_id}@example.com",
            username=f"testuser{unique_id}",
            password_hash=get_password_hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(
            name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        project = Project(
            name="Test Project",
            slug=f"test-project-{unique_id}",
            organization_id=org.id,
            created_by=user.id,
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        return user, org, project

    def test_snapshot_created_on_content_change(self, db_session):
        """Test that a snapshot is created when document content changes."""
        user, org, project = self.setup_document_context(db_session)

        # Create document
        document = Document(
            title="Test Document",
            slug="test-document",
            content="# Original\n\nContent",
            filename="test.md",
            project_id=project.id,
            organization_id=org.id,
            created_by=user.id,
            updated_by=user.id,
        )
        db_session.add(document)
        db_session.commit()
        db_session.refresh(document)

        # Update content
        document.content = "# Updated\n\nNew content"
        document.updated_by = user.id
        db_session.commit()
        db_session.refresh(document)

        # Verify snapshot was created
        snapshots = (
            db_session.query(DocumentSnapshot)
            .where(DocumentSnapshot.document_id == document.id)
            .all()
        )
        assert len(snapshots) == 1
        assert snapshots[0].old_content == "# Original\n\nContent"
        assert snapshots[0].new_content == "# Updated\n\nNew content"
        assert snapshots[0].created_by == user.id

    def test_no_snapshot_on_no_content_change(self, db_session):
        """Test that no snapshot is created when content doesn't change."""
        user, org, project = self.setup_document_context(db_session)

        # Create document
        document = Document(
            title="Test Document",
            slug="test-document",
            content="# Original\n\nContent",
            filename="test.md",
            project_id=project.id,
            organization_id=org.id,
            created_by=user.id,
            updated_by=user.id,
        )
        db_session.add(document)
        db_session.commit()
        db_session.refresh(document)

        # Update only title (not content)
        document.title = "Updated Title"
        document.updated_by = user.id
        db_session.commit()
        db_session.refresh(document)

        # Verify no snapshot was created
        snapshots = (
            db_session.query(DocumentSnapshot)
            .where(DocumentSnapshot.document_id == document.id)
            .all()
        )
        assert len(snapshots) == 0

    def test_updated_timestamp_on_update(self, db_session):
        """Test that updated_at timestamp is updated on document update."""
        user, org, project = self.setup_document_context(db_session)

        # Create document
        document = Document(
            title="Test Document",
            slug="test-document",
            content="# Original\n\nContent",
            filename="test.md",
            project_id=project.id,
            organization_id=org.id,
            created_by=user.id,
            updated_by=user.id,
        )
        db_session.add(document)
        db_session.commit()
        db_session.refresh(document)

        original_updated_at = document.updated_at

        # Update content
        import time

        time.sleep(0.01)  # Small delay to ensure timestamp difference
        document.content = "# Updated\n\nNew content"
        document.updated_by = user.id
        db_session.commit()
        db_session.refresh(document)

        # Verify updated_at changed
        assert document.updated_at > original_updated_at

    def test_multiple_snapshots_on_multiple_updates(self, db_session):
        """Test that multiple snapshots are created for multiple
        content changes in same transaction."""
        user, org, project = self.setup_document_context(db_session)

        # Create document
        document = Document(
            title="Test Document",
            slug="test-document",
            content="# Original\n\nContent",
            filename="test.md",
            project_id=project.id,
            organization_id=org.id,
            created_by=user.id,
            updated_by=user.id,
        )
        db_session.add(document)
        db_session.commit()
        db_session.refresh(document)

        # First update
        document.content = "# First Update"
        document.updated_by = user.id
        db_session.flush()

        # Second update
        document.content = "# Second Update"
        document.updated_by = user.id
        db_session.flush()

        # Third update
        document.content = "# Third Update"
        document.updated_by = user.id
        db_session.commit()

        # Verify three snapshots were created
        snapshots = (
            db_session.query(DocumentSnapshot)
            .where(DocumentSnapshot.document_id == document.id)
            .order_by(DocumentSnapshot.created_at)
            .all()
        )
        assert len(snapshots) == 3
        assert snapshots[0].old_content == "# Original\n\nContent"
        assert snapshots[0].new_content == "# First Update"
        assert snapshots[1].old_content == "# First Update"
        assert snapshots[1].new_content == "# Second Update"
        assert snapshots[2].old_content == "# Second Update"
        assert snapshots[2].new_content == "# Third Update"

    def test_snapshot_rating_copied(self, db_session):
        """Test that rating is copied to snapshot."""
        user, org, project = self.setup_document_context(db_session)

        # Create document with rating
        document = Document(
            title="Test Document",
            slug="test-document",
            content="# Original\n\nContent",
            filename="test.md",
            project_id=project.id,
            organization_id=org.id,
            created_by=user.id,
            updated_by=user.id,
            rating=5,
        )
        db_session.add(document)
        db_session.commit()
        db_session.refresh(document)

        # Update content
        document.content = "# Updated\n\nNew content"
        document.rating = 4
        document.updated_by = user.id
        db_session.commit()
        db_session.refresh(document)

        # Verify snapshot has the rating at time of update
        snapshots = (
            db_session.query(DocumentSnapshot)
            .where(DocumentSnapshot.document_id == document.id)
            .all()
        )
        assert len(snapshots) == 1
        assert snapshots[0].rating == 4

    def test_error_on_none_content(self, db_session):
        """Test that setting content to None raises ValueError."""
        user, org, project = self.setup_document_context(db_session)

        # Create document
        document = Document(
            title="Test Document",
            slug="test-document",
            content="# Original\n\nContent",
            filename="test.md",
            project_id=project.id,
            organization_id=org.id,
            created_by=user.id,
            updated_by=user.id,
        )
        db_session.add(document)
        db_session.commit()
        db_session.refresh(document)

        # Try to set content to None - should raise ValueError on flush
        document.content = None
        document.updated_by = user.id

        # Should raise ValueError during flush/commit
        with pytest.raises(ValueError, match="Document content cannot be None"):
            db_session.flush()

    def test_created_timestamp_on_insert(self, db_session):
        """Test that created_at and updated_at are set on insert."""
        user, org, project = self.setup_document_context(db_session)

        # Create document without timestamps
        document = Document(
            title="Test Document",
            slug="test-document",
            content="# Original\n\nContent",
            filename="test.md",
            project_id=project.id,
            organization_id=org.id,
            created_by=user.id,
            updated_by=user.id,
        )
        db_session.add(document)
        db_session.commit()
        db_session.refresh(document)

        # Verify timestamps are set
        assert document.created_at is not None
        assert document.updated_at is not None
