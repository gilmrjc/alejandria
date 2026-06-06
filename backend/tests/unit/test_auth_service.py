"""Unit tests for authentication business logic."""

from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt

from shared.auth.jwt import (
    create_access_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from shared.config.settings import settings


class TestPasswordHashing:
    """Test password hashing business logic."""

    def test_hash_password(self):
        """Test password hashing produces consistent result."""
        password = "my_secure_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Hashes should be different (salt)
        assert hash1 != hash2
        # Both should start with bcrypt prefix
        assert hash1.startswith("$2b$")
        assert hash2.startswith("$2b$")

    def test_verify_correct_password(self):
        """Test password verification with correct password."""
        password = "my_secure_password"
        password_hash = get_password_hash(password)

        assert verify_password(password, password_hash) is True

    def test_verify_incorrect_password(self):
        """Test password verification with incorrect password."""
        password = "my_secure_password"
        wrong_password = "wrong_password"
        password_hash = get_password_hash(password)

        assert verify_password(wrong_password, password_hash) is False

    def test_verify_password_different_hashes(self):
        """Test password verification with different hash formats."""
        password = "my_secure_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Both hashes should verify the same password
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokenCreation:
    """Test JWT token creation business logic."""

    def test_create_token(self):
        """Test token creation includes user data."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        email = "user@example.com"

        token = create_access_token(user_id=user_id, email=email)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_payload(self):
        """Test token payload contains correct data."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        email = "user@example.com"

        token = create_access_token(user_id=user_id, email=email)
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        assert payload["sub"] == user_id
        assert payload["email"] == email
        assert "exp" in payload
        assert "iat" in payload

    def test_token_expiration(self):
        """Test token has correct expiration time."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        email = "user@example.com"

        token = create_access_token(user_id=user_id, email=email)
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=UTC)
        expected_exp = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

        # Allow 1 second tolerance
        assert abs((exp_datetime - expected_exp).total_seconds()) < 1

    def test_token_issued_at(self):
        """Test token has issued at time."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        email = "user@example.com"

        token = create_access_token(user_id=user_id, email=email)
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        iat_timestamp = payload["iat"]
        iat_datetime = datetime.fromtimestamp(iat_timestamp, tz=UTC)
        now = datetime.now(UTC)

        # Allow 1 second tolerance
        assert abs((iat_datetime - now).total_seconds()) < 1


class TestJWTTokenVerification:
    """Test JWT token verification business logic."""

    def test_verify_valid_token(self):
        """Test valid token verification."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        email = "user@example.com"

        token = create_access_token(user_id=user_id, email=email)
        token_data = verify_token(token)

        assert token_data.user_id == user_id
        assert token_data.email == email

    def test_verify_invalid_token(self):
        """Test invalid token raises error."""
        invalid_token = "invalid_token_12345"

        with pytest.raises(Exception):  # noqa: B017
            # HTTPException from verify_token
            verify_token(invalid_token)

    def test_verify_token_wrong_secret(self):
        """Test token with wrong secret raises error."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        email = "user@example.com"

        token = create_access_token(user_id=user_id, email=email)

        # Try to decode with wrong secret
        with pytest.raises(Exception):  # noqa: B017
            jwt.decode(
                token,
                "wrong_secret_key",
                algorithms=[settings.algorithm],
            )

    def test_verify_token_missing_user_id(self):
        """Test token without user_id raises error."""

        # Create token without user_id
        payload = {
            "email": "user@example.com",
            "exp": datetime.now(UTC) + timedelta(hours=1),
            "iat": datetime.now(UTC),
        }
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        with pytest.raises(Exception):  # noqa: B017
            # HTTPException from verify_token
            verify_token(token)

    def test_verify_token_missing_email(self):
        """Test token without email raises error."""

        # Create token without email
        payload = {
            "sub": "123e4567-e89b-12d3-a456-426614174000",
            "exp": datetime.now(UTC) + timedelta(hours=1),
            "iat": datetime.now(UTC),
        }
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        with pytest.raises(Exception):  # noqa: B017
            # HTTPException from verify_token
            verify_token(token)

    def test_verify_expired_token(self):
        """Test expired token raises HTTPException."""
        from fastapi import HTTPException

        user_id = "123e4567-e89b-12d3-a456-426614174000"
        email = "user@example.com"

        # Create token with past expiration
        payload = {
            "sub": user_id,
            "email": email,
            "exp": datetime.now(UTC) - timedelta(hours=1),
            "iat": datetime.now(UTC) - timedelta(hours=2),
        }
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)

        assert exc_info.value.status_code == 401
