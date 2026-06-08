"""Service for grouping gaps by theme using deterministic methods."""

import logging
import uuid
from collections import defaultdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.db.models import Gap, GapTag, Tag

logger = logging.getLogger(__name__)


class GapGroupingService:
    """Service for grouping gaps by theme using deterministic methods."""

    def __init__(self, session: Session = None):
        """
        Initialize GapGroupingService.

        Args:
            session: Optional database session (must be provided for now)
        """
        self.session = session

    def group_gaps_by_tags(
        self, project_id: uuid.UUID = None, organization_id: uuid.UUID = None
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Group gaps by tags (deterministic).

        Args:
            project_id: Optional project ID filter
            organization_id: Optional organization ID filter

        Returns:
            Dictionary mapping tag names to lists of gaps
        """
        # Query gaps with their tags
        query = (
            select(Gap, Tag)
            .join(GapTag, Gap.id == GapTag.gap_id)
            .join(Tag, GapTag.tag_id == Tag.id)
        )

        if project_id:
            query = query.where(Tag.project_id == project_id)

        if organization_id:
            query = query.where(Tag.organization_id == organization_id)

        result = self.session.execute(query).all()

        # Group by tag name
        grouped = defaultdict(list)
        for gap, tag in result:
            grouped[tag.name].append(
                {
                    "id": str(gap.id),
                    "question": gap.question,
                    "priority": gap.priority,
                    "status": gap.status,
                    "document_id": str(gap.document_id),
                }
            )

        return dict(grouped)

    def get_gap_clusters(
        self, project_id: uuid.UUID = None, organization_id: uuid.UUID = None
    ) -> dict[str, Any]:
        """
        Get gap clusters using tag-based grouping (deterministic).

        Args:
            project_id: Optional project ID
            organization_id: Optional organization ID

        Returns:
            Dictionary with tag clusters
        """
        tag_clusters = self.group_gaps_by_tags(project_id, organization_id)

        return {
            "tag_clusters": tag_clusters,
        }

    def suggest_theme_tags(
        self, gap_id: uuid.UUID, top_n: int = 5
    ) -> list[dict[str, Any]]:
        """
        Suggest theme tags for a gap based on keyword matching (deterministic).

        Args:
            gap_id: Gap ID
            top_n: Number of suggestions to return

        Returns:
            List of suggested tags
        """
        # Get gap
        gap = self.session.execute(
            select(Gap).where(Gap.id == gap_id)
        ).scalar_one_or_none()

        if not gap:
            return []

        # Extract keywords from gap question
        keywords = self._extract_keywords(gap.question)

        # Check existing tags for exact keyword matches
        query = select(Tag)
        tags = self.session.execute(query).scalars().all()

        suggestions = []
        for tag in tags:
            for keyword in keywords:
                if keyword.lower() in tag.name.lower():
                    suggestions.append(
                        {
                            "tag_id": str(tag.id),
                            "tag_name": tag.name,
                        }
                    )
                    break

        return suggestions[:top_n]

    def _extract_keywords(self, text: str) -> list[str]:
        """
        Extract keywords from text (deterministic).

        Args:
            text: Text to extract keywords from

        Returns:
            List of keywords
        """
        # Deterministic keyword extraction
        # Remove common words and extract meaningful terms
        common_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "what",
            "how",
            "why",
            "when",
            "where",
            "who",
            "which",
            "that",
            "this",
            "these",
            "those",
            "with",
            "from",
            "for",
            "and",
            "or",
            "but",
        }

        words = text.lower().split()
        keywords = [
            word for word in words if word not in common_words and len(word) > 3
        ]

        return keywords
