#!/usr/bin/env python3
"""Migrate local documentation files to Alejandria via API."""

import re
import sys
from pathlib import Path
from typing import Any

import requests

API_BASE_URL = "http://localhost:8000/api/v1"
DOCS_DIR = Path("/Users/gil/projects/alejandria/docs")


def extract_title_from_content(content: str, filename: str) -> str:
    """Extract title from markdown content or use filename."""
    # Try to find first heading
    heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()

    # Fallback to filename without extension
    return filename.replace(".md", "").replace("-", " ").replace("_", " ").title()


def register_user(email: str, username: str, password: str) -> dict[str, Any]:
    """Register a new user."""
    response = requests.post(
        f"{API_BASE_URL}/auth/register",
        json={
            "email": email,
            "username": username,
            "password": password,
        },
    )
    if not response.ok:
        print(f"Registration error: {response.status_code} - {response.text}")
    response.raise_for_status()
    return response.json()


def login(email: str, password: str) -> str:
    """Login and get JWT token."""
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    response.raise_for_status()
    data = response.json()
    return data["access_token"]


def get_first_organization(token: str) -> dict[str, Any]:
    """Get the first available organization for the user."""
    response = requests.get(
        f"{API_BASE_URL}/organizations",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    orgs = response.json()
    if not orgs:
        raise Exception("No organizations found for user")
    return orgs[0]


def get_first_project(token: str) -> dict[str, Any]:
    """Get the first available project for the user."""
    response = requests.get(
        f"{API_BASE_URL}/projects",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    projects = response.json()
    if not projects:
        raise Exception("No projects found for user")
    return projects[0]


def create_project(
    token: str, name: str, slug: str, organization_id: str
) -> dict[str, Any]:
    """Create a project."""
    response = requests.post(
        f"{API_BASE_URL}/projects",
        json={
            "name": name,
            "slug": slug,
            "description": "Migrated documentation from local files",
            "organization_id": organization_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


def create_document(
    token: str,
    title: str,
    content: str,
    filename: str,
) -> dict[str, Any]:
    """Create a document."""
    response = requests.post(
        f"{API_BASE_URL}/documents",
        json={
            "title": title,
            "content": content,
            "filename": filename,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    if not response.ok:
        print(f"  Error details: {response.status_code} - {response.text}")
    response.raise_for_status()
    return response.json()


def find_markdown_files(docs_dir: Path) -> list[Path]:
    """Find all markdown files recursively."""
    markdown_files = []
    for file_path in docs_dir.rglob("*.md"):
        markdown_files.append(file_path)
    return sorted(markdown_files)


def migrate_documents():
    """Main migration function."""
    print("Starting document migration...")

    # Configuration
    email = "migrator@alejandria.dev"
    username = "doc_migrator"
    password = "MigrateDocs123!"

    try:
        # Register user (ignore if already exists)
        print(f"Registering user: {email}")
        try:
            register_user(email, username, password)
            print("User registered successfully")
        except requests.HTTPError as e:
            if e.response.status_code == 409:
                print("User already exists, proceeding with login")
            else:
                raise

        # Login
        print("Logging in...")
        token = login(email, password)
        print("Login successful")

        # Get existing organization (created during registration)
        print("Getting organization...")
        org = get_first_organization(token)
        print(f"Using organization: {org['id']} - {org['name']}")

        # Get existing project or create one
        print("Getting project...")
        try:
            project = get_first_project(token)
            print(f"Using existing project: {project['id']} - {project['name']}")
        except Exception:
            print("Creating new project...")
            try:
                project = create_project(
                    token,
                    name="System Documentation",
                    slug="system-docs",
                    organization_id=org["id"],
                )
                print(f"Project created: {project['id']}")
            except requests.HTTPError as e:
                if e.response.status_code == 409:
                    print("Project already exists, trying to get it...")
                    project = get_first_project(token)
                    print(
                        f"Using existing project: {project['id']} - {project['name']}"
                    )
                else:
                    raise

        # Find all markdown files
        print(f"Scanning {DOCS_DIR} for markdown files...")
        markdown_files = find_markdown_files(DOCS_DIR)
        print(f"Found {len(markdown_files)} markdown files")

        # Migrate each document
        success_count = 0
        error_count = 0
        skipped_count = 0

        for file_path in markdown_files:
            try:
                # Read file content
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                # Extract title
                relative_path = file_path.relative_to(DOCS_DIR)
                filename = str(relative_path)
                title = extract_title_from_content(content, file_path.name)

                print(f"Migrating: {filename}")

                # Create document
                doc = create_document(token, title, content, filename)
                print(f"  ✓ Created: {doc['id']}")
                success_count += 1

            except requests.HTTPError as e:
                if e.response.status_code == 409:
                    print(f"  ⊘ Skipped (already exists): {filename}")
                    skipped_count += 1
                else:
                    print(f"  ✗ Error migrating {file_path}: {e}")
                    error_count += 1
            except Exception as e:
                print(f"  ✗ Error migrating {file_path}: {e}")
                error_count += 1

        print("\n" + "=" * 50)
        print("Migration complete!")
        print(f"  Success: {success_count}")
        print(f"  Skipped (already exists): {skipped_count}")
        print(f"  Errors: {error_count}")
        print(f"  Total: {len(markdown_files)}")
        print("=" * 50)

    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    migrate_documents()
