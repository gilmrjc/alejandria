"""
Document versioning middleware using SQLAlchemy event listeners.

Implements automatic snapshot creation before document updates and
automatic updated_at timestamp management, following ADR-006.
"""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history

from .models import Document, DocumentSnapshot

# Attribute key for tracking old content
_OLD_CONTENT_ATTR = "_old_content"


@event.listens_for(Document, "before_update")
def handle_document_update(mapper: Any, connection: Any, target: Document) -> None:
    """
    Handle document updates: update timestamp and flag for snapshot creation.

    This event listener:
    1. Updates the updated_at timestamp on every update
    2. Validates content is not None
    3. Stores old content for comparison in after_update
    """
    # Always update timestamp
    target.updated_at = datetime.now(UTC)

    # Validate content is not None before attempting to create snapshot
    if target.content is None:
        raise ValueError("Document content cannot be None when creating snapshot")

    # Get history of content attribute to detect changes
    history = get_history(target, "content")
    if history.has_changes():
        # Store both old and new content for after_update event
        # Use instance attribute to avoid ClassVar issues
        # Store as tuple (old_content, new_content) to handle multiple updates
        old_content = history.deleted[0] if history.deleted else None
        setattr(target, _OLD_CONTENT_ATTR, (old_content, target.content))


@event.listens_for(Document, "after_update")
def create_snapshot_after_update(
    mapper: Any, connection: Any, target: Document
) -> None:
    """
    Create snapshot after document update if content changed.

    This event listener uses connection.execute() to insert the snapshot,
    avoiding SQLAlchemy warnings about Session.add() during flush.
    """
    # Get snapshot data from instance attribute
    snapshot_data = getattr(target, _OLD_CONTENT_ATTR, None)
    if snapshot_data is None:
        return

    old_content, new_content = snapshot_data

    # Only create snapshot if content actually changed
    if old_content == new_content:
        # Clean up the temporary attribute
        delattr(target, _OLD_CONTENT_ATTR)
        return

    # Insert snapshot directly using connection.execute()
    # This avoids Session.add() during flush process
    from sqlalchemy import insert

    stmt = insert(DocumentSnapshot).values(
        document_id=target.id,
        old_content=old_content,
        new_content=new_content,
        diff_type="full",  # Full snapshot for recent changes (configurable)
        rating=target.rating,
        created_by=target.updated_by,
    )
    connection.execute(stmt)

    # Clean up the temporary attribute
    delattr(target, _OLD_CONTENT_ATTR)


@event.listens_for(Document, "before_insert")
def set_created_timestamp(mapper: Any, connection: Any, target: Document) -> None:
    """
    Set created_at timestamp on insert if not already set.
    """
    if target.created_at is None:
        target.created_at = datetime.now(UTC)
    if target.updated_at is None:
        target.updated_at = datetime.now(UTC)
