#!/usr/bin/env python3
"""Create a test user for MCP testing."""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

import uuid
from sqlalchemy.orm import Session

from shared.db.models import User
from shared.db.session import get_db_session
from shared.auth.password import get_password_hash


def main():
    session = get_db_session()
    try:
        # Create test user
        user = User(
            email="mcp-test@example.com",
            username="mcp-test-user",
            password_hash=get_password_hash("testpassword123"),
            is_active=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"User created successfully!")
        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Username: {user.username}")

        return str(user.id)

    except Exception as e:
        print(f"Error creating user: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
