#!/usr/bin/env python3
"""Create an API key for the doc migrator user."""

import sys

sys.path.insert(0, "/workspace")

from sqlalchemy import select

from shared.auth.api_key import create_api_key
from shared.db.models import Organization, User
from shared.db.session import get_db_session


def main():
    session = get_db_session()
    try:
        # Find the doc_migrator user
        user = session.execute(
            select(User).where(User.username == "doc_migrator")
        ).scalar_one_or_none()

        if not user:
            print("Error: User 'doc_migrator' not found")
            print("Please run the migration script first to create the user")
            sys.exit(1)

        print(f"Found user: {user.username} (ID: {user.id})")

        # Get the user's organization
        organization = (
            session.execute(
                select(Organization).where(Organization.created_by == user.id)
            )
            .scalars()
            .first()
        )

        if not organization:
            print("Error: No organization found for user")
            sys.exit(1)

        print(f"Found organization: {organization.name} (ID: {organization.id})")

        # Create API key
        print("\nCreating API key...")
        plain_key, api_key_record = create_api_key(
            name="Documentation Migration Key",
            user_id=user.id,
            organization_id=organization.id,
            session=session,
        )

        print("\n" + "=" * 60)
        print("API Key created successfully!")
        print("=" * 60)
        print(f"Key ID: {api_key_record.id}")
        print(f"Key Name: {api_key_record.name}")
        print(f"User: {user.username}")
        print(f"Organization: {organization.name}")
        print("\n" + "=" * 60)
        print("YOUR API KEY (save this, you won't see it again):")
        print("=" * 60)
        print(f"{plain_key}")
        print("=" * 60)
        print("\nUse this key to authenticate with the MCP server")

        return plain_key

    except Exception as e:
        print(f"Error creating API key: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
