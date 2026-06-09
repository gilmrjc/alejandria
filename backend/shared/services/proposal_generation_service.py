"""Service layer for proposal generation from resolved gaps."""

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.db.models import Document, Gap, Proposal, ProposalDocument, ProposalGap

logger = logging.getLogger(__name__)


class ProposalGenerationService:
    """Service for generating proposals from resolved gaps."""

    def __init__(self, session: Session = None):
        """
        Initialize ProposalGenerationService.

        Args:
            session: Optional database session (must be provided for now)
        """
        self.session = session

    def get_resolved_gaps_since(self, timestamp: datetime) -> list[Gap]:
        """
        Get gaps with status=responded since given timestamp.

        Args:
            timestamp: Timestamp to filter gaps from

        Returns:
            List of Gap instances
        """
        query = select(Gap).where(
            Gap.status == "responded",
            Gap.answered_at >= timestamp,
        )
        result = self.session.execute(query).scalars().all()
        return list(result)

    def group_gaps_by_document(self, gaps: list[Gap]) -> dict[uuid.UUID, list[Gap]]:
        """
        Group gaps by document_id.

        Args:
            gaps: List of gaps to group

        Returns:
            Dictionary mapping document_id to list of gaps
        """
        grouped: dict[uuid.UUID, list[Gap]] = {}
        for gap in gaps:
            if gap.document_id not in grouped:
                grouped[gap.document_id] = []
            grouped[gap.document_id].append(gap)
        return grouped

    def check_existing_proposals(
        self, document_id: uuid.UUID, gap_ids: list[uuid.UUID]
    ) -> set[uuid.UUID]:
        """
        Check which gaps are already in existing proposals.

        Args:
            document_id: Document ID
            gap_ids: List of gap IDs to check

        Returns:
            Set of gap IDs that are already in proposals
        """
        # Get all proposals for this document
        proposal_docs = self.session.execute(
            select(ProposalDocument).where(ProposalDocument.document_id == document_id)
        ).scalars().all()

        proposal_ids = [pd.proposal_id for pd in proposal_docs]

        if not proposal_ids:
            return set()

        # Get all gaps in these proposals
        proposal_gaps = self.session.execute(
            select(ProposalGap).where(ProposalGap.proposal_id.in_(proposal_ids))
        ).scalars().all()

        existing_gap_ids = {pg.gap_id for pg in proposal_gaps}

        # Return intersection with requested gap_ids
        return existing_gap_ids.intersection(set(gap_ids))

    def generate_proposal_prompt(
        self, document: Document, gaps: list[Gap]
    ) -> str:
        """
        Generate LLM prompt for proposal based on document and gaps.

        Args:
            document: Document instance
            gaps: List of resolved gaps

        Returns:
            Generated prompt string
        """
        # Build gap context
        gaps_context = "\n\n".join(
            [
                f"Gap {i+1}:\n"
                f"Question: {gap.question}\n"
                f"Answer: {gap.answer}\n"
                f"Priority: {gap.priority}\n"
                f"Context Missing: {gap.context_missing or 'N/A'}\n"
                f"Role Affected: {gap.role_affected or 'N/A'}"
                for i, gap in enumerate(gaps)
            ]
        )

        prompt = f"""You are an expert technical documentation editor. Your task is to integrate the following resolved gaps into the document content.

Document Title: {document.title}
Document Slug: {document.slug}
Current Rating: {document.rating or 'Not rated'}

Resolved Gaps to Integrate:
{gaps_context}

Instructions:
1. Review the document content and the resolved gaps
2. Determine the best way to integrate each gap's answer into the document
3. Provide specific, actionable edit instructions for each gap
4. Group related edits together for efficiency
5. Specify the exact location (section/paragraph) for each edit
6. Maintain the document's existing style and structure
7. Ensure the integration improves the document's clarity and completeness

Output Format:
For each gap, provide:
- Gap ID reference
- Location in document (section/paragraph)
- Specific edit instruction (what to add/modify)
- Expected improvement in document quality

Provide the final instructions as a structured plan that can be executed to update the document."""

        return prompt

    def create_proposal(
        self,
        document_id: uuid.UUID,
        gap_ids: list[uuid.UUID],
        prompt: str,
        expected_rating: float | None = None,
    ) -> Proposal:
        """
        Create a proposal with document and gap relationships.

        Args:
            document_id: Document ID
            gap_ids: List of gap IDs to associate
            prompt: Generated prompt/instructions
            expected_rating: Expected rating after application

        Returns:
            Created Proposal instance
        """
        # Generate proposal slug
        from shared.db.models import Document

        document = self.session.execute(
            select(Document).where(Document.id == document_id)
        ).scalar_one_or_none()

        if not document:
            raise ValueError(f"Document {document_id} not found")

        slug = f"{document.slug}-proposal-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"

        # Check if slug already exists
        existing = self.session.execute(
            select(Proposal).where(Proposal.slug == slug)
        ).scalar_one_or_none()

        if existing:
            # Generate unique slug with counter
            counter = 1
            while existing:
                slug = f"{document.slug}-proposal-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}-{counter}"
                existing = self.session.execute(
                    select(Proposal).where(Proposal.slug == slug)
                ).scalar_one_or_none()
                counter += 1

        # Create proposal
        proposal = Proposal(
            slug=slug,
            name=f"Proposal for {document.title}",
            description=prompt,
            status="pending",
        )

        self.session.add(proposal)
        self.session.flush()  # Get proposal ID

        # Create ProposalDocument relationship
        proposal_doc = ProposalDocument(
            proposal_id=proposal.id,
            document_id=document_id,
        )
        self.session.add(proposal_doc)

        # Create ProposalGap relationships
        for gap_id in gap_ids:
            proposal_gap = ProposalGap(
                proposal_id=proposal.id,
                gap_id=gap_id,
            )
            self.session.add(proposal_gap)

        self.session.commit()
        self.session.refresh(proposal)

        logger.info(
            f"Created proposal {proposal.id} for document {document_id} with {len(gap_ids)} gaps"
        )

        return proposal
