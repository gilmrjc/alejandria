#!/usr/bin/env python3
"""
Script to check existing documents in database.
"""

import sys
from pathlib import Path

# Add current directory to path (running from backend/scripts)
current_path = Path(__file__).parent.parent
sys.path.insert(0, str(current_path))

from sqlalchemy import select  # noqa: E402

from shared.db.models import Document, Organization, Project  # noqa: E402
from shared.db.session import get_db_session  # noqa: E402


def main():
    session = get_db_session()
    try:
        # Get all organizations
        orgs = session.execute(select(Organization)).scalars().all()
        print(f"Organizations: {len(orgs)}")
        for org in orgs:
            print(f"  - {org.name} (slug: {org.slug}, id: {org.id})")

            # Get projects for this organization
            projects = (
                session.execute(
                    select(Project).where(Project.organization_id == org.id)
                )
                .scalars()
                .all()
            )
            print(f"    Projects: {len(projects)}")

            for project in projects:
                print(
                    f"      - {project.name} (slug: {project.slug}, id: {project.id})"
                )

                # Get documents for this project
                docs = (
                    session.execute(
                        select(Document).where(Document.project_id == project.id)
                    )
                    .scalars()
                    .all()
                )
                print(f"        Documents: {len(docs)}")

                for doc in docs:
                    print(
                        f"          - {doc.title} "
                        f"(slug: {doc.slug}, id: {doc.id}, rating: {doc.rating})"
                    )

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    main()
