"""API key management for MCP server authentication."""

import hashlib
import secrets
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.db.models import ApiKey
from shared.db.session import get_db_session


def generate_api_key() -> str:
    """
    Generate a secure random API key.

    Returns:
        API key string in format: alej_<32_random_chars>
    """
    random_bytes = secrets.token_urlsafe(32)
    return f"alej_{random_bytes}"


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for storage using SHA-256.

    Args:
        api_key: Plain text API key

    Returns:
        Hashed API key (hexadecimal string)
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_api_key(api_key: str, key_hash: str) -> bool:
    """
    Verify an API key against its hash.

    Args:
        api_key: Plain text API key
        key_hash: Stored hash of the API key

    Returns:
        True if the key matches the hash
    """
    return hash_api_key(api_key) == key_hash


def create_api_key(
    name: str,
    user_id: uuid.UUID,
    organization_id: uuid.UUID,
    session: Session | None = None,
) -> tuple[str, ApiKey]:
    """
    Create a new API key for a user.

    Args:
        name: Name/description of the API key
        user_id: User ID who owns the key
        organization_id: Organization ID for the key
        session: Optional database session (creates new if not provided)

    Returns:
        Tuple of (plain_api_key, api_key_model)
    """
    should_close = False
    if session is None:
        session = get_db_session()
        should_close = True

    try:
        # Generate and hash the API key
        plain_key = generate_api_key()
        key_hash = hash_api_key(plain_key)

        # Create API key record
        api_key = ApiKey(
            key_hash=key_hash,
            name=name,
            user_id=user_id,
            organization_id=organization_id,
            is_active=True,
        )

        session.add(api_key)
        session.commit()
        session.refresh(api_key)

        return plain_key, api_key

    finally:
        if should_close:
            session.close()


def validate_api_key(api_key: str, session: Session | None = None) -> ApiKey | None:
    """
    Validate an API key and return the associated ApiKey record.

    Args:
        api_key: Plain text API key to validate
        session: Optional database session (creates new if not provided)

    Returns:
        ApiKey record if valid and active, None otherwise
    """
    should_close = False
    if session is None:
        session = get_db_session()
        should_close = True

    try:
        # Hash the provided API key
        provided_hash = hash_api_key(api_key)

        # Direct lookup by key_hash (O(1) with unique index)
        key_record = session.execute(
            select(ApiKey).where(ApiKey.key_hash == provided_hash, ApiKey.is_active)
        ).scalar_one_or_none()

        if key_record:
            # Update last_used_at
            key_record.last_used_at = datetime.now(UTC)
            session.commit()
            return key_record

        return None

    finally:
        if should_close:
            session.close()


def revoke_api_key(api_key_id: uuid.UUID, session: Session | None = None) -> bool:
    """
    Revoke (deactivate) an API key.

    Args:
        api_key_id: ID of the API key to revoke
        session: Optional database session (creates new if not provided)

    Returns:
        True if the key was revoked
    """
    should_close = False
    if session is None:
        session = get_db_session()
        should_close = True

    try:
        api_key = session.execute(
            select(ApiKey).where(ApiKey.id == api_key_id)
        ).scalar_one_or_none()

        if api_key:
            api_key.is_active = False
            session.commit()
            return True

        return False

    finally:
        if should_close:
            session.close()
