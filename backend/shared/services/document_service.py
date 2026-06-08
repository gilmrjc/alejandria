"""Service layer for document operations."""

import logging
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.db.models import Document
from shared.db.session import get_db_session

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document business logic."""

    def __init__(self, session: Session = None):
        """
        Initialize DocumentService.

        Args:
            session: Optional database session (creates new if not provided)
        """
        self.session = session or next(get_db_session())

    def get_document(self, document_id: uuid.UUID) -> Document | None:
        """
        Get a document by ID.

        Args:
            document_id: Document ID

        Returns:
            Document instance or None
        """
        return self.session.execute(
            select(Document).where(Document.id == document_id)
        ).scalar_one_or_none()

    def get_document_by_slug(self, slug: str) -> Document | None:
        """
        Get a document by slug.

        Args:
            slug: Document slug

        Returns:
            Document instance or None
        """
        return self.session.execute(
            select(Document).where(Document.slug == slug)
        ).scalar_one_or_none()
