"""Service layer for gap operations."""

import logging
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.db.models import Gap

logger = logging.getLogger(__name__)


class GapService:
    """Service for gap business logic."""

    def __init__(self, session: Session = None):
        """
        Initialize GapService.

        Args:
            session: Optional database session (must be provided for now)
        """
        self.session = session

    def create_gap(
        self,
        document_id: uuid.UUID,
        gap_data: dict[str, Any],
    ) -> Gap:
        """
        Create a new gap.

        Args:
            document_id: Document ID
            gap_data: Gap data dictionary with question, context_missing, priority, role_affected

        Returns:
            Created Gap instance
        """
        # Generate slug from question
        question = gap_data.get("question", "")
        slug = question.lower().replace(" ", "-")[:50]

        # Check if slug already exists
        existing = self.session.execute(
            select(Gap).where(Gap.slug == slug)
        ).scalar_one_or_none()

        if existing:
            logger.warning(f"Gap with slug '{slug}' already exists, skipping")
            return None

        # Map severity to priority
        severity_to_priority = {
            "critical": "critical",
            "high": "high",
            "medium": "medium",
            "low": "low",
        }
        priority = severity_to_priority.get(
            gap_data.get("severity", "medium"), "medium"
        )

        # Create gap
        gap = Gap(
            document_id=document_id,
            slug=slug,
            question=gap_data.get("question"),
            priority=priority,
            context_missing=gap_data.get("context_missing"),
            role_affected=gap_data.get("role_affected"),
            status="pending",
        )

        self.session.add(gap)
        self.session.commit()
        self.session.refresh(gap)

        logger.info(f"Created gap {gap.id} for document {document_id}")
        return gap

    def get_gap(self, gap_id: uuid.UUID) -> Gap | None:
        """
        Get a gap by ID.

        Args:
            gap_id: Gap ID

        Returns:
            Gap instance or None
        """
        return self.session.execute(
            select(Gap).where(Gap.id == gap_id)
        ).scalar_one_or_none()

    def get_gap_by_slug(self, slug: str) -> Gap | None:
        """
        Get a gap by slug.

        Args:
            slug: Gap slug

        Returns:
            Gap instance or None
        """
        return self.session.execute(
            select(Gap).where(Gap.slug == slug)
        ).scalar_one_or_none()

    def list_gaps(
        self,
        document_id: uuid.UUID = None,
        status: str = None,
        priority: str = None,
    ) -> list[Gap]:
        """
        List gaps with optional filters.

        Args:
            document_id: Optional document ID filter
            status: Optional status filter
            priority: Optional priority filter

        Returns:
            List of Gap instances
        """
        query = select(Gap)

        if document_id is not None:
            query = query.where(Gap.document_id == document_id)

        if status is not None:
            query = query.where(Gap.status == status)

        if priority is not None:
            query = query.where(Gap.priority == priority)

        query = query.order_by(Gap.created_at.desc())

        result = self.session.execute(query).scalars().all()
        return list(result)

    def list_gaps_as_dict(
        self,
        document_id: uuid.UUID = None,
        status: str = None,
    ) -> list[dict[str, Any]]:
        """
        List gaps as dictionaries for LLM context.

        Args:
            document_id: Optional document ID filter
            status: Optional status filter

        Returns:
            List of gap dictionaries
        """
        gaps = self.list_gaps(document_id=document_id, status=status)
        return [
            {
                "id": str(gap.id),
                "question": gap.question,
                "context_missing": gap.context_missing,
                "priority": gap.priority,
                "status": gap.status,
                "role_affected": gap.role_affected,
            }
            for gap in gaps
        ]
