"""Integration tests for API endpoints."""

from shared.auth.jwt import get_password_hash
from shared.db.models import Organization, Project, User


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_login_success(self, db_session, client):
        """Test successful login."""
        # Create user
        user = User(
            email="test@example.com",
            username="testuser",
            password_hash=get_password_hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()

        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 8 * 3600

    def test_login_invalid_email(self, client):
        """Test login with invalid email."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_invalid_password(self, db_session, client):
        """Test login with invalid password."""
        user = User(
            email="test@example.com",
            username="testuser",
            password_hash=get_password_hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_inactive_user(self, db_session, client):
        """Test login with inactive user."""
        user = User(
            email="test@example.com",
            username="testuser",
            password_hash=get_password_hash("password123"),
            is_active=False,
        )
        db_session.add(user)
        db_session.commit()

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )

        assert response.status_code == 403
        assert "User account is inactive" in response.json()["detail"]

    def test_get_current_user(self, db_session, client):
        """Test getting current user info with valid token."""
        user = User(
            email="test@example.com",
            username="testuser",
            password_hash=get_password_hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()

        # Login to get token
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401


class TestDocumentEndpoints:
    """Test document endpoints."""

    def setup_document_context(self, db_session):
        """Helper to set up user, org, project for document tests."""
        import uuid

        unique_id = str(uuid.uuid4())[:8]
        user = User(
            email=f"test{unique_id}@example.com",
            username=f"testuser{unique_id}",
            password_hash=get_password_hash("password123"),
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

        project = Project(
            name="Test Project",
            slug=f"test-project-{unique_id}",
            organization_id=org.id,
            created_by=user.id,
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        return user, org, project

    def test_create_document(self, db_session, authenticated_client):
        """Test creating a document."""
        user, org, project = self.setup_document_context(db_session)

        response = authenticated_client.post(
            "/api/v1/documents",
            json={
                "title": "Test Document",
                "content": "# Test\n\nContent",
                "filename": "test.md",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Document"
        assert data["slug"] == "test-document"
        assert data["content"] == "# Test\n\nContent"

    def test_create_document_duplicate_slug(self, db_session, authenticated_client):
        """Test creating a document with duplicate slug."""
        user, org, project = self.setup_document_context(db_session)

        # Create first document
        authenticated_client.post(
            "/api/v1/documents",
            json={
                "title": "Test Document",
                "content": "# Test\n\nContent",
                "filename": "test.md",
            },
        )

        # Try to create duplicate
        response = authenticated_client.post(
            "/api/v1/documents",
            json={
                "title": "Test Document",
                "content": "# Different\n\nContent",
                "filename": "test2.md",
            },
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_get_document(self, db_session, authenticated_client):
        """Test getting a document by ID."""
        user, org, project = self.setup_document_context(db_session)

        # Create document
        create_response = authenticated_client.post(
            "/api/v1/documents",
            json={
                "title": "Test Document",
                "content": "# Test\n\nContent",
                "filename": "test.md",
            },
        )
        document_id = create_response.json()["id"]

        # Get document
        response = authenticated_client.get(f"/api/v1/documents/{document_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == document_id
        assert data["title"] == "Test Document"

    def test_get_document_not_found(self, authenticated_client):
        """Test getting a non-existent document."""
        import uuid

        fake_id = uuid.uuid4()
        response = authenticated_client.get(f"/api/v1/documents/{fake_id}")
        assert response.status_code == 404

    def test_list_documents(self, authenticated_client):
        """Test listing documents with pagination."""
        # Create multiple documents
        for i in range(5):
            authenticated_client.post(
                "/api/v1/documents",
                json={
                    "title": f"Document {i}",
                    "content": f"# Content {i}",
                    "filename": f"test{i}.md",
                },
            )

        # List documents
        response = authenticated_client.get("/api/v1/documents?page=1&per_page=3")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["per_page"] == 3
        assert data["pagination"]["total"] == 5

    def test_update_document(self, db_session, authenticated_client):
        """Test updating a document."""
        user, org, project = self.setup_document_context(db_session)

        # Create document
        create_response = authenticated_client.post(
            "/api/v1/documents",
            json={
                "title": "Test Document",
                "content": "# Test\n\nContent",
                "filename": "test.md",
            },
        )
        document_id = create_response.json()["id"]

        # Update document
        response = authenticated_client.put(
            f"/api/v1/documents/{document_id}",
            json={"title": "Updated Document", "content": "# Updated\n\nContent"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Document"
        assert data["content"] == "# Updated\n\nContent"

    def test_delete_document(self, db_session, authenticated_client):
        """Test deleting a document."""
        user, org, project = self.setup_document_context(db_session)

        # Create document
        create_response = authenticated_client.post(
            "/api/v1/documents",
            json={
                "title": "Test Document",
                "content": "# Test\n\nContent",
                "filename": "test.md",
            },
        )
        document_id = create_response.json()["id"]

        # Delete document
        response = authenticated_client.delete(f"/api/v1/documents/{document_id}")

        assert response.status_code == 204

        # Verify deletion
        get_response = authenticated_client.get(f"/api/v1/documents/{document_id}")
        assert get_response.status_code == 404


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client, monkeypatch):
        """Test health check endpoint with mocked external services."""
        # Mock external service checks to avoid hanging
        from shared.config.settings import settings

        # Use local test URLs that won't hang
        monkeypatch.setattr(settings, "qdrant_url", "http://localhost:33333")
        monkeypatch.setattr(settings, "ollama_url", "http://localhost:33334")

        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "services" in data
        assert "database" in data["services"]
        assert "redis" in data["services"]
        assert "qdrant" in data["services"]
        assert "ollama" in data["services"]
