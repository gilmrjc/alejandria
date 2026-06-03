"""
Document versioning middleware using SQLAlchemy event listeners.

Implements automatic snapshot creation before document updates and
automatic updated_at timestamp management, following ADR-006.
"""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import Session

from .models import Document, DocumentSnapshot


@event.listens_for(Document, 'before_update')
def handle_document_update(mapper: Any, connection: Any, target: Document) -> None:
    """
    Handle document updates: create snapshot if content changed and update timestamp.

    This event listener automatically:
    1. Creates a DocumentSnapshot if content has actually changed
    2. Updates the updated_at timestamp on every update
    """
    # Always update timestamp
    target.updated_at = datetime.now(timezone.utc)

    # Check if content has actually changed
    if target._old_content is None:
        # First time tracking, store current content
        target._old_content = target.content
        return

    # Only create snapshot if content actually changed
    if target.content == target._old_content:
        return

    # Validate required fields
    if target.content is None:
        raise ValueError("Document content cannot be None when creating snapshot")

    # Create snapshot record
    snapshot = DocumentSnapshot(
        document_id=target.id,
        old_content=target._old_content,
        new_content=target.content,
        diff_type='full',  # Full snapshot for recent changes (configurable)
        rating=target.rating,
        created_by=target.updated_by,
    )

    # Add to session within the same transaction
    from sqlalchemy.orm import Session as ORMSession
    session = ORMSession.object_session(target)
    session.add(snapshot)


@event.listens_for(Document, 'load')
def track_old_content(target: Document, context: Any) -> None:
    """
    Track the original content when a document is loaded.

    This allows us to compare and only create snapshots when
    content actually changes.
    """
    target._old_content = target.content


@event.listens_for(Document, 'before_insert')
def set_created_timestamp(mapper: Any, connection: Any, target: Document) -> None:
    """
    Set created_at timestamp on insert if not already set.
    """
    if target.created_at is None:
        target.created_at = datetime.now(timezone.utc)
    if target.updated_at is None:
        target.updated_at = datetime.now(timezone.utc)
