#!/usr/bin/env python3
"""Get user ID by email."""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import select  # noqa: E402

from shared.db.models import User  # noqa: E402
from shared.db.session import get_db_session  # noqa: E402


def main():
    session = get_db_session()
    try:
        # Get user by email
        user = session.execute(
            select(User).where(User.email == "dev@alejandria.local")
        ).scalar_one_or_none()

        if user:
            print(f"User ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Username: {user.username}")
            return str(user.id)
        else:
            print("User not found")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
