"""Document schemas for API request/response validation."""

import re
import unicodedata
from datetime import datetime
from uuid import UUID

import bleach
from pydantic import BaseModel, Field, field_validator


def sanitize_markdown(content: str) -> str:
    """
    Sanitize markdown content using Bleach with conservative whitelist.

    Allowed tags: p, br, strong, em, u, code, pre, blockquote, ul, ol, li, h1-h6, a
    Allowed attributes: a: href with http/https, title; code: class for syntax
    highlighting
    Allowed protocols: http, https
    """
    # Define conservative whitelist
    allowed_tags = [
        "p",
        "br",
        "strong",
        "em",
        "u",
        "code",
        "pre",
        "blockquote",
        "ul",
        "ol",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "a",
    ]

    allowed_attrs = {
        "a": ["href", "title"],
        "code": ["class"],
    }

    allowed_protocols = ["http", "https"]

    return bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=allowed_protocols,
        strip=True,
    )


def generate_slug(title: str) -> str:
    """
    Generate URL-safe slug from title.

    Algorithm:
    1. Convert to lowercase
    2. Replace spaces and non-alphanumeric characters with hyphens
    3. Remove accents and special characters (Unicode NFKD normalization)
    4. Remove consecutive hyphens
    5. Truncate to max 100 characters if necessary
    6. Ensure no leading/trailing hyphens
    """
    # Normalize Unicode (NFKD) to separate accents from characters
    normalized = unicodedata.normalize("NFKD", title)

    # Remove accents and convert to ASCII
    ascii_str = normalized.encode("ASCII", "ignore").decode("ASCII")

    # Convert to lowercase
    lower_str = ascii_str.lower()

    # Replace spaces and non-alphanumeric characters with hyphens
    hyphenated = re.sub(r"[^a-z0-9]+", "-", lower_str)

    # Remove consecutive hyphens
    single_hyphens = re.sub(r"-+", "-", hyphenated)

    # Remove leading/trailing hyphens
    slug = single_hyphens.strip("-")

    # Truncate to max 100 characters
    if len(slug) > 100:
        slug = slug[:100].rstrip("-")

    # Ensure slug is not empty
    if not slug:
        slug = "untitled"

    return slug


class DocumentBase(BaseModel):
    """Base document schema with common fields."""

    title: str = Field(..., min_length=1, max_length=500, description="Document title")
    content: str = Field(..., description="Document content (markdown)")
    filename: str = Field(
        ..., min_length=1, max_length=255, description="Document filename"
    )


class DocumentCreate(DocumentBase):
    """Schema for creating a document."""

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        """Sanitize markdown content."""
        return sanitize_markdown(v)


class DocumentUpdate(BaseModel):
    """Schema for updating a document."""

    title: str | None = Field(
        None, min_length=1, max_length=500, description="Document title"
    )
    content: str | None = Field(None, description="Document content (markdown)")
    filename: str | None = Field(
        None, min_length=1, max_length=255, description="Document filename"
    )

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, v: str | None) -> str | None:
        """Sanitize markdown content if provided."""
        if v is not None:
            return sanitize_markdown(v)
        return v


class DocumentResponse(BaseModel):
    """Schema for document response."""

    id: UUID = Field(description="Document ID")
    title: str = Field(description="Document title")
    slug: str = Field(description="URL-safe slug")
    content: str = Field(description="Document content (markdown)")
    filename: str = Field(description="Document filename")
    rating: float | None = Field(
        None, ge=0, le=10, description="Document rating (0-10)"
    )
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    created_by: UUID | None = Field(None, description="Creator user ID")
    updated_by: UUID | None = Field(None, description="Last updater user ID")

    model_config = {"from_attributes": True}


class DocumentListItem(BaseModel):
    """Schema for document list item (without full content)."""

    id: UUID = Field(description="Document ID")
    title: str = Field(description="Document title")
    slug: str = Field(description="URL-safe slug")
    filename: str = Field(description="Document filename")
    rating: float | None = Field(
        None, ge=0, le=10, description="Document rating (0-10)"
    )
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    folder_id: UUID | None = Field(None, description="Folder ID if document is in a folder")
    folder_name: str | None = Field(None, description="Folder name if document is in a folder")
    folder_path: str | None = Field(None, description="Full folder path for hierarchical display")

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):
    """Schema for paginated document list response."""

    items: list[DocumentListItem] = Field(description="List of documents")
    pagination: dict = Field(description="Pagination metadata")


class FolderTreeItem(BaseModel):
    """Schema for a folder tree item (folder or document)."""

    type: str = Field(description="Type: 'folder' or 'document'")
    id: str = Field(description="ID of the folder or document (UUID for real items, path for virtual folders)")
    name: str = Field(description="Name of the folder or document")
    path: str = Field(description="Full path for hierarchical display")
    slug: str | None = Field(None, description="Document slug (only for documents)")
    children: list["FolderTreeItem"] = Field(default_factory=list, description="Child items (only for folders)")

    model_config = {"from_attributes": True}


# Update forward references for recursive model
FolderTreeItem.model_rebuild()
