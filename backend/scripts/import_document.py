#!/usr/bin/env python3
"""
Script to import a document from filesystem to database.
"""

import sys
from pathlib import Path

# Add current directory to path (running from backend/scripts)
current_path = Path(__file__).parent.parent
sys.path.insert(0, str(current_path))

from sqlalchemy import select  # noqa: E402

from shared.db.models import Document, Organization, Project, User  # noqa: E402
from shared.db.session import get_db_session  # noqa: E402


def main():
    # Read the document
    doc_path = Path(
        "/Users/gil/projects/alejandria/docs/estrategia/estrategia/technology-strategy.md"
    )
    with open(doc_path) as f:
        content = f.read()

    # Extract title from first heading
    title = "Technology Strategy"
    for line in content.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break

    session = get_db_session()
    try:
        # Get or create organization
        org = session.execute(
            select(Organization).where(Organization.slug == "alejandria")
        ).scalar_one_or_none()

        if not org:
            # Get a user first
            user = session.execute(select(User).limit(1)).scalar_one_or_none()
            if not user:
                print("No users found in database. Please create a user first.")
                return

            org = Organization(
                name="Alejandria",
                slug="alejandria",
                created_by=user.id,
                is_personal=False,
            )
            session.add(org)
            session.commit()
            session.refresh(org)
            print(f"Created organization: {org.name} (id: {org.id})")
        else:
            print(f"Found organization: {org.name} (id: {org.id})")

        # Get or create project
        project = session.execute(
            select(Project).where(
                Project.organization_id == org.id, Project.slug == "alejandria"
            )
        ).scalar_one_or_none()

        if not project:
            user = session.execute(select(User).limit(1)).scalar_one_or_none()
            project = Project(
                organization_id=org.id,
                name="Alejandria",
                slug="alejandria",
                created_by=user.id,
                description="Proyecto principal de Alejandria",
            )
            session.add(project)
            session.commit()
            session.refresh(project)
            print(f"Created project: {project.name} (id: {project.id})")
        else:
            print(f"Found project: {project.name} (id: {project.id})")

        # Check if document already exists
        existing = session.execute(
            select(Document).where(
                Document.project_id == project.id,
                Document.slug == "technology-strategy",
            )
        ).scalar_one_or_none()

        if existing:
            print(f"Document already exists: {existing.title} (id: {existing.id})")
            print("Updating content...")
            existing.content = content
            session.commit()
            print("Document updated successfully")
            return str(existing.id)

        # Create document
        doc = Document(
            project_id=project.id,
            organization_id=org.id,
            title=title,
            slug="technology-strategy",
            content=content,
            filename="technology-strategy.md",
            rating=9.0,
        )
        session.add(doc)
        session.commit()
        session.refresh(doc)

        print("Document created successfully!")
        print(f"ID: {doc.id}")
        print(f"Title: {doc.title}")
        print(f"Slug: {doc.slug}")

        return str(doc.id)

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return None
    finally:
        session.close()


if __name__ == "__main__":
    main()
