"""Service layer for document rollback operations."""

import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.db.models import Document, DocumentSnapshot

logger = logging.getLogger(__name__)


class RollbackService:
    """Service for document rollback operations."""

    def __init__(self, session: Session = None):
        """
        Initialize RollbackService.

        Args:
            session: Optional database session (must be provided for now)
        """
        self.session = session

    def get_latest_snapshot(self, document_id: uuid.UUID) -> DocumentSnapshot | None:
        """
        Get the most recent snapshot for a document.

        Args:
            document_id: Document ID

        Returns:
            DocumentSnapshot instance or None
        """
        query = select(DocumentSnapshot).where(
            DocumentSnapshot.document_id == document_id
        ).order_by(DocumentSnapshot.created_at.desc())

        return self.session.execute(query).scalar_one_or_none()

    def get_snapshot(self, snapshot_id: uuid.UUID) -> DocumentSnapshot | None:
        """
        Get a specific snapshot by ID.

        Args:
            snapshot_id: Snapshot ID

        Returns:
            DocumentSnapshot instance or None
        """
        return self.session.execute(
            select(DocumentSnapshot).where(DocumentSnapshot.id == snapshot_id)
        ).scalar_one_or_none()

    def restore_snapshot(
        self, document_id: uuid.UUID, snapshot: DocumentSnapshot
    ) -> Document:
        """
        Restore document content from a snapshot.

        Args:
            document_id: Document ID
            snapshot: Snapshot to restore from

        Returns:
            Updated Document instance
        """
        # Get document
        document = self.session.execute(
            select(Document).where(Document.id == document_id)
        ).scalar_one_or_none()

        if not document:
            raise ValueError(f"Document {document_id} not found")

        # Create snapshot of current state before rollback
        self.create_rollback_snapshot(document_id)

        # Restore content from snapshot
        document.content = snapshot.old_content
        document.updated_at = datetime.now(UTC)

        self.session.commit()
        self.session.refresh(document)

        logger.info(f"Restored document {document_id} from snapshot {snapshot.id}")

        return document

    def create_rollback_snapshot(self, document_id: uuid.UUID) -> DocumentSnapshot:
        """
        Create a snapshot of the current document state before rollback.

        Args:
            document_id: Document ID

        Returns:
            Created DocumentSnapshot instance
        """
        # Get document
        document = self.session.execute(
            select(Document).where(Document.id == document_id)
        ).scalar_one_or_none()

        if not document:
            raise ValueError(f"Document {document_id} not found")

        # Create snapshot
        snapshot = DocumentSnapshot(
            document_id=document_id,
            old_content=document.content,
            new_content=document.content,  # Same as old for rollback snapshot
            diff_type="full",
            rating=document.rating,
            created_by=document.updated_by,
        )

        self.session.add(snapshot)
        self.session.commit()
        self.session.refresh(snapshot)

        logger.info(f"Created rollback snapshot {snapshot.id} for document {document_id}")

        return snapshot

    def rollback_to_latest(self, document_id: uuid.UUID) -> Document:
        """
        Rollback document to the latest snapshot.

        Args:
            document_id: Document ID

        Returns:
            Updated Document instance
        """
        snapshot = self.get_latest_snapshot(document_id)

        if not snapshot:
            raise ValueError(f"No snapshot found for document {document_id}")

        return self.restore_snapshot(document_id, snapshot)
