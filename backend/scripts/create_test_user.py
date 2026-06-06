#!/usr/bin/env python3
"""Create a test user for MCP testing."""

from shared.auth.password import get_password_hash

from shared.db.models import User
from shared.db.session import get_db_session


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

        print("User created successfully!")
        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Username: {user.username}")

        return str(user.id)

    except Exception as e:
        print(f"Error creating user: {e}")
        import traceback

        traceback.print_exc()
        import sys

        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
