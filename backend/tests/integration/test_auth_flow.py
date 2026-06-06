"""Integration tests for authentication flow."""

from datetime import UTC

from fastapi.testclient import TestClient

from api.main import app
from shared.auth.api_key import create_api_key, validate_api_key
from shared.auth.jwt import create_access_token, get_password_hash, verify_token
from shared.db.models import Organization, User
from shared.db.session import get_db_session


class TestJWTAuthFlow:
    """Test complete JWT authentication flow."""

    def test_complete_auth_flow(self, db_session):
        """Test complete authentication flow: register, login, access protected
        endpoint."""

        # Override database session for this test
        def override_get_db_session():
            yield db_session

        app.dependency_overrides[get_db_session] = override_get_db_session

        try:
            # Step 1: Create user (simulating registration)
            user = User(
                email="user@example.com",
                username="testuser",
                password_hash=get_password_hash("securepassword123"),
                is_active=True,
            )
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)

            # Step 2: Login
            client = TestClient(app)
            login_response = client.post(
                "/api/v1/auth/login",
                json={"email": "user@example.com", "password": "securepassword123"},
            )

            assert login_response.status_code == 200
            token_data = login_response.json()
            access_token = token_data["access_token"]
            assert token_data["token_type"] == "bearer"
            assert token_data["expires_in"] == 8 * 3600

            # Step 3: Access protected endpoint with token
            me_response = client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            assert me_response.status_code == 200
            user_data = me_response.json()
            assert user_data["email"] == "user@example.com"
            assert user_data["username"] == "testuser"
        finally:
            app.dependency_overrides.clear()

    def test_token_validation(self, db_session):
        """Test token validation with verify_token function."""
        user = User(
            email="user@example.com",
            username="testuser",
            password_hash=get_password_hash("securepassword123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Create token
        token = create_access_token(user_id=str(user.id), email=user.email)

        # Verify token
        token_data = verify_token(token)
        assert token_data.user_id == str(user.id)
        assert token_data.email == user.email

    def test_token_expiration(self):
        """Test that tokens have correct expiration."""
        from datetime import datetime, timedelta

        user_id = "test-user-id"
        email = "test@example.com"

        token = create_access_token(user_id=user_id, email=email)

        # Decode token to check expiration
        from jose import jwt

        from shared.config.settings import settings

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=UTC)
        expected_exp = datetime.now(UTC) + timedelta(hours=8)

        # Allow 1 second tolerance
        assert abs((exp_datetime - expected_exp).total_seconds()) < 1

    def test_invalid_token_rejected(self):
        """Test that invalid tokens are rejected."""
        client = TestClient(app)
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token_12345"},
        )

        assert response.status_code == 401

    def test_missing_token_rejected(self):
        """Test that requests without tokens are rejected."""
        client = TestClient(app)
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401


class TestApiKeyAuthFlow:
    """Test API key authentication flow for MCP server."""

    def test_api_key_creation_and_validation(self, db_session):
        """Test creating and validating an API key."""
        # Setup user and organization
        user = User(
            email="user@example.com",
            username="testuser",
            password_hash=get_password_hash("securepassword123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(name="Test Org", slug="test-org", created_by=user.id)
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
        assert api_key_record.is_active is True

        # Validate API key
        validated = validate_api_key(plain_key, session=db_session)
        assert validated is not None
        assert validated.id == api_key_record.id
        assert validated.last_used_at is not None

    def test_api_key_revocation(self, db_session):
        """Test revoking an API key."""
        # Setup
        user = User(
            email="user@example.com",
            username="testuser",
            password_hash=get_password_hash("securepassword123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(name="Test Org", slug="test-org", created_by=user.id)
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        plain_key, api_key_record = create_api_key(
            name="Test Key",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        # Revoke key
        from shared.auth.api_key import revoke_api_key

        result = revoke_api_key(api_key_record.id, session=db_session)
        assert result is True

        # Verify validation fails
        validated = validate_api_key(plain_key, session=db_session)
        assert validated is None

    def test_inactive_api_key_validation_fails(self, db_session):
        """Test that inactive API keys fail validation."""
        # Setup
        user = User(
            email="user@example.com",
            username="testuser",
            password_hash=get_password_hash("securepassword123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(name="Test Org", slug="test-org", created_by=user.id)
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        plain_key, api_key_record = create_api_key(
            name="Test Key",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        # Deactivate key
        api_key_record.is_active = False
        db_session.commit()

        # Validation should fail
        validated = validate_api_key(plain_key, session=db_session)
        assert validated is None

    def test_multiple_api_keys_per_user(self, db_session):
        """Test that a user can have multiple API keys."""
        # Setup
        user = User(
            email="user@example.com",
            username="testuser",
            password_hash=get_password_hash("securepassword123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(name="Test Org", slug="test-org", created_by=user.id)
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        # Create multiple keys
        key1, _ = create_api_key(
            name="Key 1",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )
        key2, _ = create_api_key(
            name="Key 2",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        # Both should be valid
        assert validate_api_key(key1, session=db_session) is not None
        assert validate_api_key(key2, session=db_session) is not None

        # Keys should be different
        assert key1 != key2


class TestAuthSecurity:
    """Test security aspects of authentication."""

    def test_password_hashing(self):
        """Test that passwords are properly hashed."""
        password = "securepassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Hashes should be different (bcrypt uses salt)
        assert hash1 != hash2

        # But both should verify correctly
        from shared.auth.jwt import verify_password

        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_wrong_password_verification_fails(self):
        """Test that wrong passwords fail verification."""
        password = "securepassword123"
        wrong_password = "wrongpassword"
        password_hash = get_password_hash(password)

        from shared.auth.jwt import verify_password

        assert verify_password(wrong_password, password_hash) is False

    def test_inactive_user_cannot_login(self, db_session):
        """Test that inactive users cannot login."""

        # Override database session for this test
        def override_get_db_session():
            yield db_session

        app.dependency_overrides[get_db_session] = override_get_db_session

        try:
            user = User(
                email="user@example.com",
                username="testuser",
                password_hash=get_password_hash("securepassword123"),
                is_active=False,
            )
            db_session.add(user)
            db_session.commit()

            client = TestClient(app)
            response = client.post(
                "/api/v1/auth/login",
                json={"email": "user@example.com", "password": "securepassword123"},
            )

            assert response.status_code == 403
            assert "inactive" in response.json()["detail"].lower()
        finally:
            app.dependency_overrides.clear()

    def test_api_key_uniqueness(self, db_session):
        """Test that API key hashes are unique."""
        # Setup
        user = User(
            email="user@example.com",
            username="testuser",
            password_hash=get_password_hash("securepassword123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        org = Organization(name="Test Org", slug="test-org", created_by=user.id)
        db_session.add(org)
        db_session.commit()
        db_session.refresh(org)

        # Create multiple keys
        _, key1 = create_api_key(
            name="Key 1",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )
        _, key2 = create_api_key(
            name="Key 2",
            user_id=user.id,
            organization_id=org.id,
            session=db_session,
        )

        # Hashes should be unique
        assert key1.key_hash != key2.key_hash
