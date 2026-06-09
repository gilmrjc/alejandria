"""Service layer for applying proposal instructions to documents."""

import logging
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.db.models import Document, Proposal, ProposalDocument, ProposalGap

logger = logging.getLogger(__name__)


class ProposalApplicationService:
    """Service for applying proposal instructions to documents."""

    def __init__(self, session: Session = None):
        """
        Initialize ProposalApplicationService.

        Args:
            session: Optional database session (must be provided for now)
        """
        self.session = session

    def get_proposal(self, proposal_id: uuid.UUID) -> Proposal | None:
        """
        Get a proposal by ID.

        Args:
            proposal_id: Proposal ID

        Returns:
            Proposal instance or None
        """
        return self.session.execute(
            select(Proposal).where(Proposal.id == proposal_id)
        ).scalar_one_or_none()

    def get_proposal_documents(self, proposal_id: uuid.UUID) -> list[Document]:
        """
        Get all documents associated with a proposal.

        Args:
            proposal_id: Proposal ID

        Returns:
            List of Document instances
        """
        proposal_docs = self.session.execute(
            select(ProposalDocument).where(ProposalDocument.proposal_id == proposal_id)
        ).scalars().all()

        document_ids = [pd.document_id for pd in proposal_docs]

        if not document_ids:
            return []

        documents = self.session.execute(
            select(Document).where(Document.id.in_(document_ids))
        ).scalars().all()

        return list(documents)

    def apply_proposal_instructions(
        self, document: Document, instructions: str
    ) -> str:
        """
        Apply proposal instructions to a document using LLM.

        Args:
            document: Document instance
            instructions: Proposal instructions/description

        Returns:
            Updated document content
        """
        # This will be called from the Celery task with async LLM
        # The service method is synchronous, the LLM call happens in the task
        return instructions

    def update_document_rating(
        self, document_id: uuid.UUID, new_rating: float | None
    ) -> Document:
        """
        Update document rating.

        Args:
            document_id: Document ID
            new_rating: New rating value

        Returns:
            Updated Document instance
        """
        document = self.session.execute(
            select(Document).where(Document.id == document_id)
        ).scalar_one_or_none()

        if not document:
            raise ValueError(f"Document {document_id} not found")

        document.rating = new_rating

        self.session.commit()
        self.session.refresh(document)

        logger.info(f"Updated rating for document {document_id} to {new_rating}")

        return document

    def mark_proposal_implemented(self, proposal_id: uuid.UUID) -> Proposal:
        """
        Mark a proposal as implemented.

        Args:
            proposal_id: Proposal ID

        Returns:
            Updated Proposal instance
        """
        proposal = self.session.execute(
            select(Proposal).where(Proposal.id == proposal_id)
        ).scalar_one_or_none()

        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")

        proposal.status = "implemented"

        self.session.commit()
        self.session.refresh(proposal)

        logger.info(f"Marked proposal {proposal_id} as implemented")

        return proposal

    def mark_proposal_failed(
        self, proposal_id: uuid.UUID, error_message: str
    ) -> Proposal:
        """
        Mark a proposal as failed.

        Args:
            proposal_id: Proposal ID
            error_message: Error message to append to description

        Returns:
            Updated Proposal instance
        """
        proposal = self.session.execute(
            select(Proposal).where(Proposal.id == proposal_id)
        ).scalar_one_or_none()

        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")

        proposal.status = "failed"
        proposal.description = f"{proposal.description}\n\nApplication failed: {error_message}"

        self.session.commit()
        self.session.refresh(proposal)

        logger.error(f"Marked proposal {proposal_id} as failed: {error_message}")

        return proposal
