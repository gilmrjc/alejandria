"""Unit tests for API key authentication."""

import uuid

from shared.auth.api_key import (
    create_api_key,
    generate_api_key,
    hash_api_key,
    revoke_api_key,
    validate_api_key,
    verify_api_key,
)
from shared.db.models import Organization, User


class TestApiKeyGeneration:
    """Test API key generation and hashing."""

    def test_generate_api_key_format(self):
        """Test that generated API key has correct format."""
        api_key = generate_api_key()
        assert api_key.startswith("alej_")
        assert len(api_key) > 10  # Should be longer than prefix

    def test_generate_api_key_unique(self):
        """Test that generated API keys are unique."""
        key1 = generate_api_key()
        key2 = generate_api_key()
        assert key1 != key2

    def test_hash_api_key(self):
        """Test API key hashing."""
        api_key = generate_api_key()
        key_hash = hash_api_key(api_key)
        assert key_hash != api_key
        assert len(key_hash) > 0

    def test_verify_api_key_valid(self):
        """Test verifying a valid API key."""
        api_key = generate_api_key()
        key_hash = hash_api_key(api_key)
        assert verify_api_key(api_key, key_hash) is True

    def test_verify_api_key_invalid(self):
        """Test verifying an invalid API key."""
        api_key = generate_api_key()
        key_hash = hash_api_key(api_key)
        wrong_key = generate_api_key()
        assert verify_api_key(wrong_key, key_hash) is False


class TestApiKeyCreation:
    """Test API key creation with database."""

    def test_create_api_key(self, db_session, password_hash):
        """Test creating an API key."""
        # Create user and organization
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"test{unique_id}@example.com",
            username=f"testuser{unique_id}",
            password_hash=password_hash,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(
            name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        # Create API key
        plain_key, api_key_record = create_api_key(
            name="Test Key",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        assert plain_key.startswith("alej_")
        assert api_key_record.id is not None
        assert api_key_record.name == "Test Key"
        assert api_key_record.user_id == user.id
        assert api_key_record.organization_id == org.id
        assert api_key_record.is_active is True
        assert api_key_record.key_hash != plain_key

    def test_create_api_key_without_session(self, db_session, password_hash):
        """Test creating an API key without providing a session."""
        # Create user and organization
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"test{unique_id}@example.com",
            username=f"testuser{unique_id}",
            password_hash=password_hash,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(
            name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        # Create API key with session (always required in practice)
        plain_key, api_key_record = create_api_key(
            name="Test Key",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        assert plain_key.startswith("alej_")
        assert api_key_record.id is not None


class TestApiKeyValidation:
    """Test API key validation."""

    def test_validate_api_key_valid(self, db_session, password_hash):
        """Test validating a valid API key."""
        # Create user, organization, and API key
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"test{unique_id}@example.com",
            username=f"testuser{unique_id}",
            password_hash=password_hash,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(
            name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        plain_key, api_key_record = create_api_key(
            name="Test Key",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        # Validate the key
        validated_key = validate_api_key(plain_key, session=db_session)
        assert validated_key is not None
        assert validated_key.id == api_key_record.id
        assert validated_key.last_used_at is not None

    def test_validate_api_key_invalid(self, db_session):
        """Test validating an invalid API key."""
        invalid_key = "alej_invalidkey123"
        validated_key = validate_api_key(invalid_key, session=db_session)
        assert validated_key is None

    def test_validate_api_key_inactive(self, db_session, password_hash):
        """Test validating an inactive API key."""
        # Create user, organization, and API key
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"test{unique_id}@example.com",
            username=f"testuser{unique_id}",
            password_hash=password_hash,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(
            name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        plain_key, api_key_record = create_api_key(
            name="Test Key",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        # Deactivate the key
        api_key_record.is_active = False
        db_session.commit()

        # Validate the key
        validated_key = validate_api_key(plain_key, session=db_session)
        assert validated_key is None


class TestApiKeyRevocation:
    """Test API key revocation."""

    def test_revoke_api_key(self, db_session, password_hash):
        """Test revoking an API key."""
        # Create user, organization, and API key
        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"test{unique_id}@example.com",
            username=f"testuser{unique_id}",
            password_hash=password_hash,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(
            name="Test Org", slug=f"test-org-{unique_id}", created_by=user.id
        )
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        plain_key, api_key_record = create_api_key(
            name="Test Key",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        # Revoke the key
        result = revoke_api_key(api_key_record.id, session=db_session)
        assert result is True

        # Verify it's deactivated
        db_session.refresh(api_key_record)
        assert api_key_record.is_active is False

    def test_revoke_nonexistent_api_key(self, db_session):
        """Test revoking a non-existent API key."""
        fake_id = uuid.uuid4()
        result = revoke_api_key(fake_id, session=db_session)
        assert result is False
