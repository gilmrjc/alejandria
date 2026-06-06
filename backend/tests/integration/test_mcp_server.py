"""Integration tests for MCP server tools."""

import sys
import uuid
from pathlib import Path

import pytest

from shared.auth.jwt import get_password_hash
from shared.db.models import (
    Document,
    Gap,
    Organization,
    Project,
    User,
)

# Import MCP server functions directly from the module file
mcp_path = Path(__file__).parent.parent.parent / "mcp_server" / "server.py"
spec = __import__("importlib.util").util.spec_from_file_location("mcp_server", mcp_path)
mcp_server = __import__("importlib.util").util.module_from_spec(spec)
sys.modules["mcp_server"] = mcp_server
spec.loader.exec_module(mcp_server)


@pytest.fixture(autouse=True)
def setup_test_session(db_session):
    """Set up test session for MCP server functions."""
    mcp_server.set_test_session(db_session)
    yield
    mcp_server.set_test_session(None)


class TestMCPDocumentTools:
    """Test MCP server document-related tools."""

    def setup_document_context(self, db_session):
        """Helper to set up user, org, project, and document for MCP tests."""
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"mcp{unique_id}@example.com",
            username=f"mcpuser{unique_id}",
            password_hash=get_password_hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(
            name="MCP Test Org", slug=f"mcp-test-org-{unique_id}", created_by=user.id
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        project = Project(
            name="MCP Test Project",
            slug=f"mcp-test-project-{unique_id}",
            organization_id=org.id,
            created_by=user.id,
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        document = Document(
            title="Test Document",
            slug="test-document",
            content="# Test\n\nContent",
            filename="test.md",
            project_id=project.id,
            organization_id=org.id,
            created_by=user.id,
        )
        db_session.add(document)
        db_session.commit()
        db_session.refresh(document)

        return user, org, project, document

    def test_read_document(self, db_session):
        """Test reading a document via MCP tool."""
        user, org, project, document = self.setup_document_context(db_session)

        result = mcp_server.read_document(document.slug, include_metadata=False)

        assert result["id"] == str(document.id)
        assert result["title"] == "Test Document"
        assert result["content"] == "# Test\n\nContent"
        assert result["filename"] == "test.md"
        assert "created_by" not in result

    def test_read_document_with_metadata(self, db_session):
        """Test reading a document with metadata via MCP tool."""
        user, org, project, document = self.setup_document_context(db_session)

        result = mcp_server.read_document(document.slug, include_metadata=True)

        assert result["id"] == str(document.id)
        assert result["created_by"] == str(user.id)
        assert result["rating"] is None

    def test_read_document_not_found(self, db_session):
        """Test reading a non-existent document."""
        with pytest.raises(ValueError, match="not found"):
            mcp_server.read_document("non-existent-slug")

    def test_write_document(self, db_session):
        """Test updating document content via MCP tool."""
        user, org, project, document = self.setup_document_context(db_session)

        result = mcp_server.write_document(
            str(document.id),
            "# Updated\n\nNew content",
            "Test update",
        )

        assert result["id"] == str(document.id)
        assert result["content"] == "# Updated\n\nNew content"
        # Version is the number of snapshots created
        # (may be >1 if middleware created snapshot during setup)
        assert result["version"] >= 1

    def test_write_document_not_found(self, db_session):
        """Test writing to a non-existent document."""
        fake_id = uuid.uuid4()
        with pytest.raises(ValueError, match="not found"):
            mcp_server.write_document(str(fake_id), "content", "message")


class TestMCPGapTools:
    """Test MCP server gap-related tools."""

    def setup_gap_context(self, db_session):
        """Helper to set up document for gap tests."""
        doc_tools = TestMCPDocumentTools()
        user, org, project, document = doc_tools.setup_document_context(db_session)
        return user, org, project, document

    def test_list_gaps(self, db_session):
        """Test listing gaps for a document."""
        user, org, project, document = self.setup_gap_context(db_session)

        # Create a gap
        gap = Gap(
            document_id=document.id,
            slug="test-gap-list",
            question="What is the architecture?",
            context_missing="No architecture description",
            priority="high",
            status="pending",
        )
        db_session.add(gap)
        db_session.commit()

        result = mcp_server.list_gaps(document.slug)

        assert result["total"] == 1
        assert len(result["gaps"]) == 1
        assert result["gaps"][0]["question"] == "What is the architecture?"

    def test_list_gaps_with_status_filter(self, db_session):
        """Test listing gaps with status filter."""
        user, org, project, document = self.setup_gap_context(db_session)

        # Create gaps with different statuses
        gap1 = Gap(
            document_id=document.id,
            slug="test-gap-1",
            question="Question 1",
            context_missing="Missing 1",
            priority="high",
            status="pending",
        )
        gap2 = Gap(
            document_id=document.id,
            slug="test-gap-2",
            question="Question 2",
            context_missing="Missing 2",
            priority="medium",
            status="responded",
        )
        db_session.add_all([gap1, gap2])
        db_session.commit()

        result = mcp_server.list_gaps(document.slug, status="pending")

        assert result["total"] == 1
        assert result["gaps"][0]["status"] == "pending"

    def test_create_gap(self, db_session):
        """Test creating a gap via MCP tool."""
        user, org, project, document = self.setup_gap_context(db_session)

        result = mcp_server.create_gap(
            document_slug=document.slug,
            question="What is the authentication mechanism?",
            context_missing="No auth documentation",
            priority="critical",
            role_affected="developer",
        )

        assert result["document_id"] == str(document.id)
        assert result["question"] == "What is the authentication mechanism?"
        assert result["priority"] == "critical"
        assert result["status"] == "pending"
        assert result["role_affected"] == "developer"

    def test_create_gap_invalid_document(self, db_session):
        """Test creating a gap for non-existent document."""
        uuid.uuid4()
        with pytest.raises(ValueError, match="not found"):
            mcp_server.create_gap(
                document_slug="non-existent-slug",
                question="Question",
                context_missing="Missing",
            )

    def test_answer_gap(self, db_session):
        """Test answering a gap via MCP tool."""
        user, org, project, document = self.setup_gap_context(db_session)

        # Create a gap
        gap = Gap(
            document_id=document.id,
            slug="test-gap-answer",
            question="What is the architecture?",
            context_missing="No architecture description",
            priority="high",
            status="pending",
        )
        db_session.add(gap)
        db_session.commit()
        db_session.refresh(gap)

        result = mcp_server.answer_gap(
            gap.slug, "The architecture is microservices-based"
        )

        assert result["id"] == str(gap.id)
        assert result["answer"] == "The architecture is microservices-based"
        assert result["status"] == "responded"
        assert result["answered_at"] is not None

    def test_answer_gap_already_answered(self, db_session):
        """Test answering an already answered gap."""
        user, org, project, document = self.setup_gap_context(db_session)

        # Create and answer a gap
        gap = Gap(
            document_id=document.id,
            slug="test-gap-already-answered",
            question="Question",
            context_missing="Missing",
            priority="high",
            status="responded",
            answer="Already answered",
        )
        db_session.add(gap)
        db_session.commit()

        with pytest.raises(ValueError, match="already answered"):
            mcp_server.answer_gap(gap.slug, "New answer")


class TestMCPTagTools:
    """Test MCP server tag-related tools."""

    def setup_tag_context(self, db_session):
        """Helper to set up project for tag tests."""
        doc_tools = TestMCPDocumentTools()
        user, org, project, document = doc_tools.setup_document_context(db_session)
        return user, org, project, document

    def test_create_tag(self, db_session):
        """Test creating a tag via MCP tool."""
        user, org, project, document = self.setup_tag_context(db_session)

        result = mcp_server.create_tag(
            name="security",
            project_id=str(project.id),
            organization_id=str(org.id),
        )

        assert result["name"] == "security"
        assert result["created_at"] is not None

    def test_assign_tag_to_gap(self, db_session):
        """Test assigning a tag to a gap via MCP tool."""
        user, org, project, document = self.setup_tag_context(db_session)

        # Create a gap
        gap = Gap(
            document_id=document.id,
            slug="test-gap-tag-assign",
            question="Question",
            context_missing="Missing",
            priority="high",
            status="pending",
        )
        db_session.add(gap)
        db_session.commit()
        db_session.refresh(gap)

        # Create a tag
        tag_result = mcp_server.create_tag(
            name="security",
            project_id=str(project.id),
            organization_id=str(org.id),
        )
        tag_result["id"]

        result = mcp_server.assign_tag_to_gap(gap.slug, tag_result["slug"])

        assert result["gap_slug"] == gap.slug
        assert result["tag_slug"] == tag_result["slug"]
        assert "assigned_at" in result

    def test_assign_tag_to_gap_already_assigned(self, db_session):
        """Test assigning an already assigned tag."""
        user, org, project, document = self.setup_tag_context(db_session)

        # Create a gap
        gap = Gap(
            document_id=document.id,
            slug="test-gap-tag-already-assigned",
            question="Question",
            context_missing="Missing",
            priority="high",
            status="pending",
        )
        db_session.add(gap)
        db_session.commit()
        db_session.refresh(gap)

        # Create a tag
        tag_result = mcp_server.create_tag(
            name="security",
            project_id=str(project.id),
            organization_id=str(org.id),
        )
        tag_result["id"]

        # Assign tag first time
        mcp_server.assign_tag_to_gap(gap.slug, tag_result["slug"])

        # Try to assign again
        result = mcp_server.assign_tag_to_gap(gap.slug, tag_result["slug"])

        assert result["message"] == "Tag already assigned to gap"

    def test_list_gaps_by_tag(self, db_session):
        """Test listing gaps by tag via MCP tool."""
        user, org, project, document = self.setup_tag_context(db_session)

        # Create gaps
        gap1 = Gap(
            document_id=document.id,
            slug="test-gap-tag-1",
            question="Question 1",
            context_missing="Missing 1",
            priority="high",
            status="pending",
        )
        gap2 = Gap(
            document_id=document.id,
            slug="test-gap-tag-2",
            question="Question 2",
            context_missing="Missing 2",
            priority="medium",
            status="pending",
        )
        db_session.add_all([gap1, gap2])
        db_session.commit()
        db_session.refresh(gap1)
        db_session.refresh(gap2)

        # Create a tag
        tag_result = mcp_server.create_tag(
            name="security",
            project_id=str(project.id),
            organization_id=str(org.id),
        )
        tag_result["id"]

        # Assign tag to first gap only
        mcp_server.assign_tag_to_gap(gap1.slug, tag_result["slug"])

        result = mcp_server.list_gaps_by_tag(tag_result["slug"])

        assert result["total"] == 1
        assert result["gaps"][0]["id"] == str(gap1.id)


class TestMCPProposalTools:
    """Test MCP server proposal-related tools."""

    def setup_proposal_context(self, db_session):
        """Helper to set up context for proposal tests."""
        doc_tools = TestMCPDocumentTools()
        user, org, project, document = doc_tools.setup_document_context(db_session)

        # Create gaps
        gap1 = Gap(
            document_id=document.id,
            slug="test-gap-proposal-1",
            question="Question 1",
            context_missing="Missing 1",
            priority="high",
            status="pending",
        )
        gap2 = Gap(
            document_id=document.id,
            slug="test-gap-proposal-2",
            question="Question 2",
            context_missing="Missing 2",
            priority="medium",
            status="pending",
        )
        db_session.add_all([gap1, gap2])
        db_session.commit()
        db_session.refresh(gap1)
        db_session.refresh(gap2)

        return user, org, project, document, gap1, gap2

    def test_create_proposal(self, db_session):
        """Test creating a proposal via MCP tool."""
        user, org, project, document, gap1, gap2 = self.setup_proposal_context(
            db_session
        )

        import json

        result = mcp_server.create_proposal(
            name="Add authentication documentation",
            description="Add comprehensive authentication docs",
            gap_slugs=json.dumps([gap1.slug, gap2.slug]),
        )

        assert result["name"] == "Add authentication documentation"
        assert result["status"] == "pending"
        assert result["gap_count"] == 2
        assert result["created_at"] is not None

    def test_create_proposal_invalid_gap(self, db_session):
        """Test creating a proposal with invalid gap ID."""
        user, org, project, document, gap1, gap2 = self.setup_proposal_context(
            db_session
        )

        import json

        with pytest.raises(ValueError, match="not found"):
            mcp_server.create_proposal(
                name="Test",
                description="Test",
                gap_slugs=json.dumps([gap1.slug, "non-existent-slug"]),
            )


class TestMCPQuestionTools:
    """Test MCP server question-related tools."""

    def setup_question_context(self, db_session):
        """Helper to set up context for question tests."""
        doc_tools = TestMCPDocumentTools()
        user, org, project, document = doc_tools.setup_document_context(db_session)
        return user, org, project, document

    def test_create_question(self, db_session):
        """Test creating a question via MCP tool."""
        user, org, project, document = self.setup_question_context(db_session)

        result = mcp_server.create_question(
            project_id=str(project.id),
            organization_id=str(org.id),
            question_text="What is the system architecture?",
            document_id=str(document.id),
        )

        assert result["question"] == "What is the system architecture?"
        assert result["status"] == "pending"
        assert result["document_id"] == str(document.id)

    def test_create_question_without_document(self, db_session):
        """Test creating a question without document reference."""
        user, org, project, document = self.setup_question_context(db_session)

        result = mcp_server.create_question(
            project_id=str(project.id),
            organization_id=str(org.id),
            question_text="What is the system architecture?",
        )

        assert result["document_id"] is None


class TestMCPOrganizationTools:
    """Test MCP server organization-related tools."""

    def setup_organization_context(self, db_session):
        """Helper to set up user for organization tests."""
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"org{unique_id}@example.com",
            username=f"orguser{unique_id}",
            password_hash=get_password_hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def test_create_organization(self, db_session):
        """Test creating an organization via MCP tool."""
        user = self.setup_organization_context(db_session)

        result = mcp_server.create_organization(
            name="Test Organization",
            slug="test-org",
            created_by=str(user.id),
            is_personal=False,
        )

        assert result["name"] == "Test Organization"
        assert result["slug"] == "test-org"
        assert result["is_personal"] is False
        assert "id" in result
        assert "created_at" in result

    def test_create_organization_duplicate_slug(self, db_session):
        """Test creating an organization with duplicate slug."""
        user = self.setup_organization_context(db_session)

        mcp_server.create_organization(
            name="Test Organization",
            slug="test-org",
            created_by=str(user.id),
        )

        with pytest.raises(ValueError, match="already exists"):
            mcp_server.create_organization(
                name="Another Organization",
                slug="test-org",
                created_by=str(user.id),
            )

    def test_get_organization_by_slug(self, db_session):
        """Test getting an organization by slug via MCP tool."""
        user = self.setup_organization_context(db_session)

        # Create organization
        org = Organization(
            name="Test Organization",
            slug="test-org",
            created_by=user.id,
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        result = mcp_server.get_organization_by_slug("test-org")

        assert result["id"] == str(org.id)
        assert result["slug"] == "test-org"
        assert result["name"] == "Test Organization"

    def test_get_organization_by_slug_not_found(self, db_session):
        """Test getting a non-existent organization."""
        with pytest.raises(ValueError, match="not found"):
            mcp_server.get_organization_by_slug("non-existent")


class TestMCPProjectTools:
    """Test MCP server project-related tools."""

    def setup_project_context(self, db_session):
        """Helper to set up org for project tests."""
        org_tools = TestMCPOrganizationTools()
        user = org_tools.setup_organization_context(db_session)

        org = Organization(
            name="Test Organization",
            slug="test-org",
            created_by=user.id,
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        return user, org

    def test_create_project(self, db_session):
        """Test creating a project via MCP tool."""
        user, org = self.setup_project_context(db_session)

        result = mcp_server.create_project(
            organization_id=str(org.id),
            name="Test Project",
            slug="test-project",
            created_by=str(user.id),
            description="A test project",
        )

        assert result["name"] == "Test Project"
        assert result["slug"] == "test-project"
        assert result["description"] == "A test project"
        assert result["organization_id"] == str(org.id)
        assert "id" in result
        assert "created_at" in result

    def test_create_project_duplicate_slug(self, db_session):
        """Test creating a project with duplicate slug in same org."""
        user, org = self.setup_project_context(db_session)

        mcp_server.create_project(
            organization_id=str(org.id),
            name="Test Project",
            slug="test-project",
            created_by=str(user.id),
        )

        with pytest.raises(ValueError, match="already exists"):
            mcp_server.create_project(
                organization_id=str(org.id),
                name="Another Project",
                slug="test-project",
                created_by=str(user.id),
            )

    def test_get_project_by_slug(self, db_session):
        """Test getting a project by slugs via MCP tool."""
        user, org = self.setup_project_context(db_session)

        project = Project(
            name="Test Project",
            slug="test-project",
            organization_id=org.id,
            created_by=user.id,
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        result = mcp_server.get_project_by_slug("test-org", "test-project")

        assert result["id"] == str(project.id)
        assert result["slug"] == "test-project"
        assert result["name"] == "Test Project"
        assert result["organization_id"] == str(org.id)

    def test_get_project_by_slug_org_not_found(self, db_session):
        """Test getting a project with non-existent organization."""
        with pytest.raises(ValueError, match="not found"):
            mcp_server.get_project_by_slug("non-existent", "test-project")

    def test_get_project_by_slug_project_not_found(self, db_session):
        """Test getting a non-existent project."""
        user, org = self.setup_project_context(db_session)

        with pytest.raises(ValueError, match="not found"):
            mcp_server.get_project_by_slug("test-org", "non-existent")


class TestMCPCreateDocument:
    """Test MCP server create_document tool."""

    def setup_document_create_context(self, db_session):
        """Helper to set up project for document creation tests."""
        org_tools = TestMCPOrganizationTools()
        user = org_tools.setup_organization_context(db_session)

        org = Organization(
            name="Test Organization",
            slug="test-org",
            created_by=user.id,
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        project = Project(
            name="Test Project",
            slug="test-project",
            organization_id=org.id,
            created_by=user.id,
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        return user, org, project

    def test_create_document(self, db_session):
        """Test creating a document via MCP tool."""
        user, org, project = self.setup_document_create_context(db_session)

        result = mcp_server.create_document(
            project_id=str(project.id),
            organization_id=str(org.id),
            title="Test Document",
            slug="test-document",
            content="# Test\n\nContent",
            filename="test.md",
            rating=4.5,
        )

        assert result["title"] == "Test Document"
        assert result["slug"] == "test-document"
        assert result["content"] == "# Test\n\nContent"
        assert result["filename"] == "test.md"
        assert result["rating"] == 4.5
        assert "id" in result
        assert "created_at" in result
        assert "updated_at" in result

    def test_create_document_duplicate_slug(self, db_session):
        """Test creating a document with duplicate slug."""
        user, org, project = self.setup_document_create_context(db_session)

        mcp_server.create_document(
            project_id=str(project.id),
            organization_id=str(org.id),
            title="Test Document",
            slug="test-document",
            content="# Test",
            filename="test.md",
        )

        with pytest.raises(ValueError, match="already exists"):
            mcp_server.create_document(
                project_id=str(project.id),
                organization_id=str(org.id),
                title="Another Document",
                slug="test-document",
                content="# Another",
                filename="another.md",
            )


class TestMCPGetCurrentUser:
    """Test MCP server get_current_user tool."""

    def setup_user_context(self, db_session):
        """Helper to set up user with API key."""
        from shared.auth.api_key import create_api_key

        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"user{unique_id}@example.com",
            username=f"testuser{unique_id}",
            password_hash=get_password_hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(
            name="Test Organization",
            slug=f"test-org-{unique_id}",
            created_by=user.id,
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        plain_key, api_key = create_api_key(
            name="Test API Key",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        return user, org, api_key

    def test_get_current_user(self, db_session):
        """Test getting current user via MCP tool."""
        user, org, api_key = self.setup_user_context(db_session)

        result = mcp_server.get_current_user()

        assert result["user_id"] == str(user.id)
        assert result["username"] == user.username
        assert result["email"] == user.email
        assert result["organization_id"] == str(org.id)
        assert result["organization_slug"] == org.slug
        assert result["organization_name"] == org.name


class TestMCPSearchTools:
    """Test MCP server search tools."""

    def setup_search_context(self, db_session):
        """Helper to set up context for search tests."""
        doc_tools = TestMCPDocumentTools()
        user, org, project, document = doc_tools.setup_document_context(db_session)
        return user, org, project, document

    def test_search_similar_documents(self, db_session, monkeypatch):
        """Test searching similar documents via MCP tool using BM25."""
        user, org, project, document = self.setup_search_context(db_session)

        # Mock Qdrant client to avoid external dependency
        from shared.config.settings import settings

        monkeypatch.setattr(settings, "qdrant_url", "http://localhost:33333")

        # Mock the QdrantClient for BM25 search
        class MockQdrantClient:
            def search_similar(
                self, collection_name, query_text, limit, score_threshold
            ):
                return [
                    {
                        "id": f"{document.id}_chunk_0",
                        "score": 0.85,
                        "payload": {
                            "document_id": str(document.id),
                            "chunk_index": 0,
                            "content": "# Test\n\nContent",
                        },
                    }
                ]

        import shared.vector.qdrant as qdrant_module

        original_client = qdrant_module.QdrantClient

        qdrant_module.QdrantClient = MockQdrantClient

        try:
            result = mcp_server.search_similar_documents(
                query="test query",
                project_id=str(project.id),
                limit=5,
            )

            assert result["query"] == "test query"
            assert result["total"] == 1
            assert len(result["results"]) == 1
            assert result["results"][0]["id"] == str(document.id)
            assert result["results"][0]["score"] == 0.85
        finally:
            qdrant_module.QdrantClient = original_client

    def test_search_similar_documents_invalid_project(self, db_session):
        """Test searching with invalid project ID."""
        fake_id = uuid.uuid4()
        with pytest.raises(ValueError, match="not found"):
            mcp_server.search_similar_documents(
                query="test",
                project_id=str(fake_id),
            )
