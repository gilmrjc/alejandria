"""Unit tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from shared.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    generate_slug,
    sanitize_markdown,
)
from shared.schemas.gap import GapCreate, GapUpdate
from shared.schemas.user import UserCreate, UserLogin


class TestDocumentSchemas:
    """Test document schemas."""

    def test_generate_slug_basic(self):
        """Test basic slug generation."""
        assert generate_slug("Technical Brief") == "technical-brief"
        assert generate_slug("API Documentation") == "api-documentation"

    def test_generate_slug_with_special_chars(self):
        """Test slug generation with special characters."""
        assert generate_slug("¿Por qué usar REST?") == "por-que-usar-rest"
        assert generate_slug("API (v1)") == "api-v1"

    def test_generate_slug_long_title(self):
        """Test slug generation truncates long titles."""
        long_title = "A" * 150
        slug = generate_slug(long_title)
        assert len(slug) <= 100
        assert slug == "a" * 100

    def test_sanitize_markdown_basic(self):
        """Test basic markdown sanitization."""
        content = "# Title\n\nParagraph with **bold** text."
        sanitized = sanitize_markdown(content)
        assert "# Title" in sanitized
        assert "**bold**" in sanitized

    def test_sanitize_markdown_removes_script(self):
        """Test that script tags are removed."""
        content = "<script>alert('xss')</script>"
        sanitized = sanitize_markdown(content)
        assert "<script>" not in sanitized
        # Note: Bleach removes the tag but not the content inside
        # The content is escaped but not removed
        assert sanitized == "alert('xss')"

    def test_document_create_valid(self):
        """Test valid document creation schema."""
        data = {
            "title": "Test Document",
            "content": "# Test\n\nContent here",
            "filename": "test.md",
        }
        doc = DocumentCreate(**data)
        assert doc.title == "Test Document"
        assert doc.content == "# Test\n\nContent here"

    def test_document_create_sanitizes_content(self):
        """Test that document creation sanitizes content."""
        data = {
            "title": "Test Document",
            "content": "<script>alert('xss')</script>",
            "filename": "test.md",
        }
        doc = DocumentCreate(**data)
        assert "<script>" not in doc.content

    def test_document_create_invalid_title(self):
        """Test that empty title raises validation error."""
        with pytest.raises(ValidationError):
            DocumentCreate(
                title="",
                content="Content",
                filename="test.md",
            )

    def test_document_update_partial(self):
        """Test partial document update."""
        data = {"title": "Updated Title"}
        doc = DocumentUpdate(**data)
        assert doc.title == "Updated Title"
        assert doc.content is None
        assert doc.filename is None


class TestUserSchemas:
    """Test user schemas."""

    def test_user_create_valid(self):
        """Test valid user creation."""
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepassword123",
        }
        user = UserCreate(**data)
        assert user.email == "test@example.com"
        assert user.username == "testuser"

    def test_user_create_invalid_email(self):
        """Test that invalid email raises validation error."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email",
                username="testuser",
                password="securepassword123",
            )

    def test_user_create_invalid_username(self):
        """Test that invalid username raises validation error."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                username="invalid username!",
                password="securepassword123",
            )

    def test_user_create_short_password(self):
        """Test that short password raises validation error."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                username="testuser",
                password="short",
            )

    def test_user_login_valid(self):
        """Test valid user login schema."""
        data = {
            "email": "test@example.com",
            "password": "securepassword123",
        }
        login = UserLogin(**data)
        assert login.email == "test@example.com"
        assert login.password == "securepassword123"


class TestGapSchemas:
    """Test gap schemas."""

    def test_gap_create_valid(self):
        """Test valid gap creation."""
        data = {
            "document_id": "123e4567-e89b-12d3-a456-426614174000",
            "question": "What is the architecture?",
            "priority": "high",
            "context_missing": "No architecture description found",
        }
        gap = GapCreate(**data)
        assert gap.question == "What is the architecture?"
        assert gap.priority == "high"

    def test_gap_create_invalid_priority(self):
        """Test that invalid priority raises validation error."""
        data = {
            "document_id": "123e4567-e89b-12d3-a456-426614174000",
            "question": "What is the architecture?",
            "priority": "invalid",
        }
        with pytest.raises(ValidationError):
            GapCreate(**data)

    def test_gap_update_valid(self):
        """Test valid gap update."""
        data = {
            "answer": "The architecture is based on 5 phases.",
            "status": "responded",
        }
        gap = GapUpdate(**data)
        assert gap.answer == "The architecture is based on 5 phases."
        assert gap.status == "responded"

    def test_gap_update_invalid_status(self):
        """Test that invalid status raises validation error."""
        data = {"status": "invalid"}
        with pytest.raises(ValidationError):
            GapUpdate(**data)
