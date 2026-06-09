"""
MCP Server implementation using FastMCP.

Implements tools for document management, gap detection, and resolution
according to mcp-tools-specification.md (ARC-036).
"""

import contextlib
import logging
import os
import uuid

from fastmcp import FastMCP
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from shared.auth.api_key import validate_api_key
from shared.db.models import (
    Document,
    Gap,
    GapDocumentReference,
    GapTag,
    Organization,
    Project,
    Proposal,
    ProposalGap,
    Question,
    QuestionDocumentReference,
    Tag,
)
from shared.db.session import get_db_session
from shared.schemas.document import generate_slug

# Create MCP server
mcp = FastMCP("Alejandria MCP Server")

# API key authentication (for HTTP transport mode)
API_KEY_REQUIRED = os.getenv("MCP_API_KEY_REQUIRED", "false").lower() == "true"

# Session cache for better performance
_session_cache: dict[str, Session] = {}

# Test session for integration tests
_test_session: Session | None = None

# Dependency injection for database session (for testing)
_db_session_provider = get_db_session


def set_test_session(session: Session | None):
    """
    Set a test database session for integration tests.

    This allows integration tests to inject a test database session
    that will be used instead of creating a new session.

    Args:
        session: Database session to use for testing, or None to reset
    """
    global _test_session
    _test_session = session


def set_db_session_provider(provider):
    """
    Set a custom database session provider (for testing).

    This allows integration tests to inject a test database session.

    Args:
        provider: Function that returns a database session
    """
    global _db_session_provider
    _db_session_provider = provider


def reset_db_session_provider():
    """Reset the database session provider to the default."""
    global _db_session_provider
    _db_session_provider = get_db_session


def get_authenticated_session(api_key: str | None = None) -> tuple[Session, bool]:
    """
    Get a database session with API key authentication and caching.

    Args:
        api_key: API key from Authorization header (for HTTP transport)

    Returns:
        Tuple of (session, should_close) where should_close indicates if
        the caller should close the session

    Raises:
        ValueError: If API key authentication fails
    """
    # Use test session if available (for integration tests)
    if _test_session is not None:
        return _test_session, False

    if API_KEY_REQUIRED and api_key:
        # Validate API key for HTTP transport
        key_record = validate_api_key(api_key)
        if not key_record:
            raise ValueError("Invalid or inactive API key")

    # Use cached session if available for this API key
    cache_key = api_key or "default"
    if cache_key in _session_cache:
        session = _session_cache[cache_key]
        try:
            # Test if session is still alive
            session.execute(text("SELECT 1"))
            return session, False
        except Exception:
            # Session is dead, remove from cache
            del _session_cache[cache_key]

    # Create new session
    session = get_db_session()
    _session_cache[cache_key] = session
    return session, True


def close_all_sessions():
    """Close all cached sessions. Call this on shutdown."""
    for session in _session_cache.values():
        with contextlib.suppress(Exception):
            session.close()
    _session_cache.clear()


@mcp.tool()
def get_current_user() -> dict:
    """
    Get the current authenticated user from API key.

    Returns:
        Current user data including user_id, username, and organization info
        from API key
    """
    # This is a temporary workaround - in production, FastMCP should pass
    # the API key from request context
    # For now, we'll get the API key from the first active record
    session, should_close = get_authenticated_session()
    try:
        from shared.db.models import ApiKey, Organization, User

        # Get the first active API key (temporary workaround)
        api_key = session.execute(
            select(ApiKey).where(ApiKey.is_active).limit(1)
        ).scalar_one_or_none()

        if not api_key:
            raise ValueError("No active API key found")

        # Get the user
        user = session.execute(
            select(User).where(User.id == api_key.user_id)
        ).scalar_one_or_none()

        if not user:
            raise ValueError("User not found for API key")

        # Get the organization associated with this API key
        organization = session.execute(
            select(Organization).where(Organization.id == api_key.organization_id)
        ).scalar_one_or_none()

        if not organization:
            raise ValueError("Organization not found for API key")

        return {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "organization_id": str(organization.id),
            "organization_slug": organization.slug,
            "organization_name": organization.name,
            "organization_is_personal": organization.is_personal,
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def read_document(document_slug: str, include_metadata: bool = False) -> dict:
    """
    Read a document by slug.

    Args:
        document_slug: Slug of the document
        include_metadata: Whether to include metadata in response

    Returns:
        Document data with content and optional metadata
    """
    session, should_close = get_authenticated_session()

    try:
        doc = session.execute(
            select(Document).where(Document.slug == document_slug)
        ).scalar_one_or_none()

        if not doc:
            raise ValueError(f"Document with slug '{document_slug}' not found")

        response = {
            "id": str(doc.id),
            "slug": doc.slug,
            "title": doc.title,
            "content": doc.content,
            "filename": doc.filename,
            "created_at": doc.created_at.isoformat(),
            "updated_at": doc.updated_at.isoformat(),
        }

        if include_metadata:
            response["created_by"] = str(doc.created_by) if doc.created_by else None
            response["updated_by"] = str(doc.updated_by) if doc.updated_by else None
            response["rating"] = doc.rating

        return response

    finally:
        if should_close:
            session.close()


@mcp.tool()
def create_organization(
    name: str, slug: str, created_by: str, is_personal: bool = False
) -> dict:
    """
    Create a new organization.

    Args:
        name: Organization name
        slug: Organization slug (unique identifier)
        created_by: UUID of the user creating the organization
        is_personal: Whether this is a personal organization

    Returns:
        Created organization data
    """
    session, should_close = get_authenticated_session()
    try:
        # Check if organization with this slug already exists
        existing = session.execute(
            select(Organization).where(Organization.slug == slug)
        ).scalar_one_or_none()

        if existing:
            raise ValueError(f"Organization with slug '{slug}' already exists")

        # Create organization
        org = Organization(
            name=name,
            slug=slug,
            created_by=uuid.UUID(created_by),
            is_personal=is_personal,
        )

        session.add(org)
        session.commit()
        session.refresh(org)

        return {
            "id": str(org.id),
            "slug": org.slug,
            "name": org.name,
            "is_personal": org.is_personal,
            "created_at": org.created_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def create_project(
    organization_id: str,
    name: str,
    slug: str,
    created_by: str,
    description: str | None = None,
) -> dict:
    """
    Create a new project.

    Args:
        organization_id: UUID of the organization
        name: Project name
        slug: Project slug (unique within organization)
        created_by: UUID of the user creating the project
        description: Optional project description

    Returns:
        Created project data
    """
    session, should_close = get_authenticated_session()
    try:
        # Check if project with this slug already exists in the organization
        existing = session.execute(
            select(Project).where(
                Project.organization_id == uuid.UUID(organization_id),
                Project.slug == slug,
            )
        ).scalar_one_or_none()

        if existing:
            raise ValueError(
                f"Project with slug '{slug}' already exists in this organization"
            )

        # Create project
        project = Project(
            organization_id=uuid.UUID(organization_id),
            name=name,
            slug=slug,
            created_by=uuid.UUID(created_by),
            description=description,
        )

        session.add(project)
        session.commit()
        session.refresh(project)

        return {
            "id": str(project.id),
            "slug": project.slug,
            "name": project.name,
            "description": project.description,
            "organization_id": str(project.organization_id),
            "created_at": project.created_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def get_organization_by_slug(slug: str) -> dict:
    """
    Get an organization by slug.

    Args:
        slug: Organization slug

    Returns:
        Organization data
    """
    session, should_close = get_authenticated_session()
    try:
        org = session.execute(
            select(Organization).where(Organization.slug == slug)
        ).scalar_one_or_none()

        if not org:
            raise ValueError(f"Organization with slug '{slug}' not found")

        return {
            "id": str(org.id),
            "slug": org.slug,
            "name": org.name,
            "is_personal": org.is_personal,
            "created_at": org.created_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def get_project_by_slug(organization_slug: str, project_slug: str) -> dict:
    """
    Get a project by organization and project slugs.

    Args:
        organization_slug: Organization slug
        project_slug: Project slug

    Returns:
        Project data
    """
    session, should_close = get_authenticated_session()
    try:
        # First get organization by slug
        org = session.execute(
            select(Organization).where(Organization.slug == organization_slug)
        ).scalar_one_or_none()

        if not org:
            raise ValueError(f"Organization with slug '{organization_slug}' not found")

        # Then get project by slug within that organization
        project = session.execute(
            select(Project).where(
                Project.organization_id == org.id,
                Project.slug == project_slug,
            )
        ).scalar_one_or_none()

        if not project:
            raise ValueError(f"Project with slug '{project_slug}' not found")

        return {
            "id": str(project.id),
            "slug": project.slug,
            "name": project.name,
            "description": project.description,
            "organization_id": str(project.organization_id),
            "created_at": project.created_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def create_document(
    project_id: str,
    organization_id: str,
    title: str,
    slug: str,
    content: str,
    filename: str,
    folder_id: str | None = None,
    rating: float | None = None,
) -> dict:
    """
    Create a new document.

    Args:
        project_id: UUID of the project
        organization_id: UUID of the organization
        title: Document title
        slug: Document slug (unique identifier)
        content: Document content
        filename: Original filename
        folder_id: Optional UUID of the folder
        rating: Optional document rating

    Returns:
        Created document data
    """
    session, should_close = get_authenticated_session()
    try:
        # Check if document with this slug already exists
        existing = session.execute(
            select(Document).where(Document.slug == slug)
        ).scalar_one_or_none()

        if existing:
            raise ValueError(f"Document with slug '{slug}' already exists")

        # Create document
        doc = Document(
            project_id=uuid.UUID(project_id),
            organization_id=uuid.UUID(organization_id),
            folder_id=uuid.UUID(folder_id) if folder_id else None,
            title=title,
            slug=slug,
            content=content,
            filename=filename,
            rating=rating,
        )

        session.add(doc)
        session.commit()
        session.refresh(doc)

        return {
            "id": str(doc.id),
            "slug": doc.slug,
            "title": doc.title,
            "content": doc.content,
            "filename": doc.filename,
            "rating": doc.rating,
            "created_at": doc.created_at.isoformat(),
            "updated_at": doc.updated_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def write_document(document_id: str, content: str, commit_message: str) -> dict:
    """
    Update document content. Accepts either UUID or slug.

    Args:
        document_id: UUID or slug of the document
        content: New content for the document
        commit_message: Message describing the change

    Returns:
        Updated document data
    """
    session, should_close = get_authenticated_session()
    try:
        # Try to find document by UUID first, then by slug
        try:
            doc = session.execute(
                select(Document).where(Document.id == uuid.UUID(document_id))
            ).scalar_one_or_none()
        except ValueError:
            # Not a valid UUID, try by slug
            doc = session.execute(
                select(Document).where(Document.slug == document_id)
            ).scalar_one_or_none()

        if not doc:
            raise ValueError(f"Document {document_id} not found")

        # Update content (middleware will create snapshot automatically)
        doc.content = content
        session.commit()
        session.refresh(doc)

        # Count snapshots to determine version
        from shared.db.models import DocumentSnapshot

        snapshot_count = (
            session.execute(
                select(func.count())
                .select_from(DocumentSnapshot)
                .where(DocumentSnapshot.document_id == doc.id)
            ).scalar()
            or 0
        )
        version = snapshot_count + 1

        return {
            "id": str(doc.id),
            "slug": doc.slug,
            "title": doc.title,
            "content": doc.content,
            "filename": doc.filename,
            "updated_at": doc.updated_at.isoformat(),
            "version": version,
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def list_gaps(document_slug: str, status: str | None = None) -> dict:
    """
    List gaps for a document, optionally filtered by status.

    Args:
        document_slug: Slug of the document
        status: Optional status filter (pending, responded, rejected)

    Returns:
        List of gaps with total count
    """
    session, should_close = get_authenticated_session()
    try:
        # Get document by slug
        doc = session.execute(
            select(Document).where(Document.slug == document_slug)
        ).scalar_one_or_none()

        if not doc:
            raise ValueError(f"Document with slug '{document_slug}' not found")

        query = select(Gap).where(Gap.document_id == doc.id)

        if status:
            query = query.where(Gap.status == status)

        gaps = session.execute(query).scalars().all()

        return {
            "gaps": [
                {
                    "id": str(gap.id),
                    "slug": gap.slug,
                    "question": gap.question,
                    "priority": gap.priority,
                    "status": gap.status,
                    "created_at": gap.created_at.isoformat(),
                }
                for gap in gaps
            ],
            "total": len(gaps),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def create_gap(
    document_slug: str,
    question: str,
    context_missing: str,
    priority: str = "medium",
    role_affected: str | None = None,
    answer: str | None = None,
    document_ids: str | None = None,
) -> dict:
    """
    Create a new gap for a document.

    Args:
        document_slug: Slug of the document
        question: The gap question
        context_missing: Description of missing context
        priority: Gap priority (critical, high, medium, low)
        role_affected: Role affected by this gap
        answer: Optional suggested answer pre-filled by LLM (status stays pending)
        document_ids: Optional JSON string list of document UUIDs used as references for gap generation


    Returns:
        Created gap data
    """
    import json

    session, should_close = get_authenticated_session()
    try:
        # Verify document exists by slug
        doc = session.execute(
            select(Document).where(Document.slug == document_slug)
        ).scalar_one_or_none()

        if not doc:
            raise ValueError(f"Document with slug '{document_slug}' not found")

        # Generate unique slug for gap
        import hashlib

        gap_slug = f"gap-{hashlib.md5(question.encode()).hexdigest()[:12]}"

        # Check if gap with this slug already exists
        existing = session.execute(
            select(Gap).where(Gap.slug == gap_slug)
        ).scalar_one_or_none()

        if existing:
            raise ValueError(f"Gap with slug '{gap_slug}' already exists")

        # Create gap
        gap = Gap(
            document_id=doc.id,
            slug=gap_slug,
            question=question,
            context_missing=context_missing,
            priority=priority,
            role_affected=role_affected,
            answer=answer,
            status="pending",
        )

        session.add(gap)
        session.commit()
        session.refresh(gap)

        # Link gap to documents if provided
        if document_ids:
            # Parse JSON string to list
            try:
                doc_ids_list = json.loads(document_ids)
            except json.JSONDecodeError:
                # If not valid JSON, try comma-separated string
                doc_ids_list = [s.strip() for s in document_ids.split(",")]

            # Verify all documents exist
            docs = (
                session.execute(
                    select(Document).where(Document.id.in_([uuid.UUID(did) for did in doc_ids_list]))
                )
                .scalars()
                .all()
            )

            if len(docs) != len(doc_ids_list):
                raise ValueError("One or more documents not found")

            # Create gap-document references
            for ref_doc in docs:
                gdr = GapDocumentReference(
                    gap_id=gap.id,
                    document_id=ref_doc.id,
                )
                session.add(gdr)

            session.commit()

        return {
            "id": str(gap.id),
            "slug": gap.slug,
            "document_id": str(doc.id),
            "document_slug": document_slug,
            "question": gap.question,
            "context_missing": gap.context_missing,
            "priority": gap.priority,
            "role_affected": gap.role_affected,
            "answer": gap.answer,
            "status": gap.status,
            "created_at": gap.created_at.isoformat(),
            "reference_document_count": len(doc_ids_list) if document_ids else 0,
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def answer_gap(gap_slug: str, answer: str) -> dict:
    """
    Answer a gap question.

    Args:
        gap_slug: Slug of the gap
        answer: The answer to the gap question


    Returns:
        Updated gap data
    """
    session, should_close = get_authenticated_session()
    try:
        gap = session.execute(
            select(Gap).where(Gap.slug == gap_slug)
        ).scalar_one_or_none()

        if not gap:
            raise ValueError(f"Gap with slug '{gap_slug}' not found")

        if gap.status == "responded":
            raise ValueError(f"Gap with slug '{gap_slug}' is already answered")

        gap.answer = answer
        gap.status = "responded"
        # Set answered_at timestamp
        from datetime import UTC, datetime

        gap.answered_at = datetime.now(UTC)

        session.commit()
        session.refresh(gap)

        return {
            "id": str(gap.id),
            "question": gap.question,
            "answer": gap.answer,
            "status": gap.status,
            "answered_at": gap.answered_at.isoformat() if gap.answered_at else None,
            "answered_by": str(gap.answered_by) if gap.answered_by else None,
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def create_tag(name: str, project_id: str, organization_id: str) -> dict:
    """
    Create a new tag for classifying gaps.

    Args:
        name: Tag name
        project_id: UUID of the project
        organization_id: UUID of the organization


    Returns:
        Created tag data
    """
    session, should_close = get_authenticated_session()
    try:
        # Generate unique slug for tag
        import hashlib

        tag_slug = f"tag-{hashlib.md5(name.encode()).hexdigest()[:12]}"

        # Check if tag with this slug already exists
        existing = session.execute(
            select(Tag).where(Tag.slug == tag_slug)
        ).scalar_one_or_none()

        if existing:
            raise ValueError(f"Tag with slug '{tag_slug}' already exists")

        tag = Tag(
            name=name,
            slug=tag_slug,
            project_id=uuid.UUID(project_id),
            organization_id=uuid.UUID(organization_id),
        )

        session.add(tag)
        session.commit()
        session.refresh(tag)

        return {
            "id": str(tag.id),
            "slug": tag.slug,
            "name": tag.name,
            "created_at": tag.created_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def assign_tag_to_gap(gap_slug: str, tag_slug: str) -> dict:
    """
    Assign a tag to a gap.

    Args:
        gap_slug: Slug of the gap
        tag_slug: Slug of the tag


    Returns:
        Assignment confirmation
    """
    session, should_close = get_authenticated_session()
    try:
        # Verify gap and tag exist by slug
        gap = session.execute(
            select(Gap).where(Gap.slug == gap_slug)
        ).scalar_one_or_none()

        if not gap:
            raise ValueError(f"Gap with slug '{gap_slug}' not found")

        tag = session.execute(
            select(Tag).where(Tag.slug == tag_slug)
        ).scalar_one_or_none()

        if not tag:
            raise ValueError(f"Tag with slug '{tag_slug}' not found")

        # Check if assignment already exists
        existing = session.execute(
            select(GapTag).where(
                GapTag.gap_id == gap.id,
                GapTag.tag_id == tag.id,
            )
        ).scalar_one_or_none()

        if existing:
            return {
                "gap_slug": gap_slug,
                "tag_slug": tag_slug,
                "assigned_at": existing.created_at.isoformat(),
                "message": "Tag already assigned to gap",
            }

        # Create assignment
        gap_tag = GapTag(
            gap_id=gap.id,
            tag_id=tag.id,
        )

        session.add(gap_tag)
        session.commit()
        session.refresh(gap_tag)

        return {
            "gap_slug": gap_slug,
            "tag_slug": tag_slug,
            "assigned_at": gap_tag.created_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def list_gaps_by_tag(tag_slug: str, status: str | None = None) -> dict:
    """
    List gaps associated with a specific tag.

    Args:
        tag_slug: Slug of the tag
        status: Optional status filter


    Returns:
        List of gaps with total count
    """
    session, should_close = get_authenticated_session()
    try:
        # Get tag by slug
        tag = session.execute(
            select(Tag).where(Tag.slug == tag_slug)
        ).scalar_one_or_none()

        if not tag:
            raise ValueError(f"Tag with slug '{tag_slug}' not found")

        query = select(Gap).join(GapTag).where(GapTag.tag_id == tag.id)

        if status:
            query = query.where(Gap.status == status)

        gaps = session.execute(query).scalars().all()

        return {
            "gaps": [
                {
                    "id": str(gap.id),
                    "slug": gap.slug,
                    "question": gap.question,
                    "priority": gap.priority,
                    "status": gap.status,
                }
                for gap in gaps
            ],
            "total": len(gaps),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def create_proposal(
    name: str,
    description: str,
    gap_slugs: str,
) -> dict:
    """
    Create a new proposal to resolve gaps.

    Args:
        name: Proposal name
        description: Detailed description of the proposal
        gap_slugs: JSON string list of gap slugs this proposal addresses


    Returns:
        Created proposal data
    """
    import json

    # Parse JSON string to list
    try:
        gap_slugs_list = json.loads(gap_slugs)
    except json.JSONDecodeError:
        # If not valid JSON, try comma-separated string
        gap_slugs_list = [s.strip() for s in gap_slugs.split(",")]

    session, should_close = get_authenticated_session()
    try:
        # Verify all gaps exist by slug
        gaps = (
            session.execute(select(Gap).where(Gap.slug.in_(gap_slugs_list)))
            .scalars()
            .all()
        )

        if len(gaps) != len(gap_slugs_list):
            raise ValueError("One or more gaps not found")

        # Generate unique slug for proposal
        import hashlib

        proposal_slug = f"proposal-{hashlib.md5(name.encode()).hexdigest()[:12]}"

        # Check if proposal with this slug already exists
        existing = session.execute(
            select(Proposal).where(Proposal.slug == proposal_slug)
        ).scalar_one_or_none()

        if existing:
            raise ValueError(f"Proposal with slug '{proposal_slug}' already exists")

        # Create proposal
        proposal = Proposal(
            slug=proposal_slug,
            name=name,
            description=description,
            status="pending",
        )

        session.add(proposal)
        session.commit()
        session.refresh(proposal)

        # Link proposal to gaps
        for gap in gaps:
            proposal_gap = ProposalGap(
                proposal_id=proposal.id,
                gap_id=gap.id,
            )
            session.add(proposal_gap)

        session.commit()

        return {
            "id": str(proposal.id),
            "slug": proposal.slug,
            "name": proposal.name,
            "description": proposal.description,
            "status": proposal.status,
            "gap_count": len(gap_slugs_list),
            "created_at": proposal.created_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def create_question(
    project_id: str,
    organization_id: str,
    question_text: str,
    document_id: str | None = None,
) -> dict:
    """
    Create a question for a project.

    Args:
        project_id: UUID of the project
        organization_id: UUID of the organization
        question_text: The question text
        document_id: Optional UUID of a document to reference


    Returns:
        Created question data
    """
    session, should_close = get_authenticated_session()
    try:
        # Generate slug from question text
        slug = generate_slug(question_text[:100])  # Truncate to 100 chars for slug

        # Create question
        question = Question(
            project_id=uuid.UUID(project_id),
            organization_id=uuid.UUID(organization_id),
            slug=slug,
            question=question_text,
            status="pending",
        )

        session.add(question)
        session.commit()
        session.refresh(question)

        # Link question to document if provided
        if document_id:
            # Verify document exists
            doc = session.execute(
                select(Document).where(Document.id == uuid.UUID(document_id))
            ).scalar_one_or_none()

            if not doc:
                raise ValueError(f"Document {document_id} not found")

            qdr = QuestionDocumentReference(
                question_id=question.id,
                document_id=uuid.UUID(document_id),
            )
            session.add(qdr)
            session.commit()

        return {
            "id": str(question.id),
            "question": question.question,
            "status": question.status,
            "project_id": project_id,
            "organization_id": organization_id,
            "document_id": document_id,
            "created_at": question.created_at.isoformat(),
        }

    finally:
        if should_close:
            session.close()


@mcp.tool()
def search_similar_documents(
    query: str,
    project_id: str,
    limit: int = 5,
    use_hybrid: bool = True,
) -> dict:
    """
    Search for similar documents using hybrid search (BM25 + semantic) or BM25 only.

    When use_hybrid=True, combines BM25 keyword search with semantic vector search
    using Reciprocal Rank Fusion (RRF) for better results.

    Args:
        query: Search query text
        project_id: UUID of the project to search within
        limit: Maximum number of results (default: 5)
        use_hybrid: Whether to use hybrid search (default: True)


    Returns:
        List of similar documents with similarity scores
    """
    import asyncio
    from shared.vector.qdrant import QdrantClient, generate_embedding

    session, should_close = get_authenticated_session()
    try:
        # Verify project exists
        from shared.db.models import Project

        project = session.execute(
            select(Project).where(Project.id == uuid.UUID(project_id))
        ).scalar_one_or_none()

        if not project:
            raise ValueError(f"Project {project_id} not found")

        qdrant_client = QdrantClient()
        collection_name = f"project_{project_id}_hybrid"

        results = []
        search_type = "bm25"

        # Check if we can use hybrid search (requires async context for embeddings)
        can_use_hybrid = False
        if use_hybrid:
            try:
                # Check if there's already a running event loop
                asyncio.get_running_loop()
                # If we're in an async context, we can't use asyncio.run()
                logger.warning("Running in async context, falling back to BM25-only search")
            except RuntimeError:
                # No running loop, we can use asyncio.run
                can_use_hybrid = True
                logger.info("No running event loop, can use hybrid search")

        if can_use_hybrid:
            try:
                # Try hybrid search (BM25 + semantic)
                # Generate embedding for query
                logger.info(f"Attempting hybrid search on collection: {collection_name}")
                query_vector = asyncio.run(generate_embedding(query))
                logger.info(f"Generated query embedding successfully")

                # Attempt hybrid search
                results = qdrant_client.search_hybrid(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    query_text=query,
                    limit=limit,
                )
                search_type = "hybrid"
                logger.info(f"Hybrid search returned {len(results)} results")
            except Exception as e:
                # Hybrid search failed, fallback to BM25 on hybrid collection
                logger.warning(f"Hybrid search failed, falling back to BM25: {e}")
                collection_name_hybrid = f"project_{project_id}_hybrid"
                logger.info(f"Using BM25 fallback on collection: {collection_name_hybrid}")
                results = qdrant_client.search_similar(
                    collection_name=collection_name_hybrid,
                    query_text=query,
                    limit=limit,
                    score_threshold=0.0,
                )
                search_type = "bm25"
                logger.info(f"BM25 fallback returned {len(results)} results")
        else:
            # Use BM25 only on hybrid collection (documents are stored in hybrid collections)
            collection_name_hybrid = f"project_{project_id}_hybrid"
            logger.info(f"Using BM25 search on collection: {collection_name_hybrid}")
            results = qdrant_client.search_similar(
                collection_name=collection_name_hybrid,
                query_text=query,
                limit=limit,
                score_threshold=0.0,
            )
            logger.info(f"BM25 search returned {len(results)} results")
            search_type = "bm25"

        # Get document details for each result
        # Extract document_id from payload instead of parsing point ID
        document_ids = []
        for r in results:
            payload = r.get("payload", {})
            doc_id = payload.get("document_id")
            if doc_id:
                document_ids.append(doc_id)
        
        documents = {}
        if document_ids:
            from shared.db.models import Document

            doc_results = (
                session.execute(
                    select(Document).where(
                        Document.id.in_(
                            [uuid.UUID(did) for did in document_ids]
                        )
                    )
                )
                .scalars()
                .all()
            )
            documents = {str(doc.id): doc for doc in doc_results}

        # Format results
        formatted_results = []
        for result in results:
            # Extract document_id from payload
            payload = result.get("payload", {})
            doc_id = payload.get("document_id")
            doc = documents.get(doc_id) if doc_id else None
            if doc:
                result_data = {
                    "id": str(doc.id),
                    "title": doc.title,
                    "slug": doc.slug,
                    "score": result["score"],
                    "chunk_content": result["payload"].get("content", ""),
                }
                # Add individual scores if hybrid search
                if search_type == "hybrid":
                    result_data["dense_score"] = result.get("dense_score", 0)
                    result_data["sparse_score"] = result.get("sparse_score", 0)
                formatted_results.append(result_data)

        return {
            "query": query,
            "results": formatted_results,
            "total": len(formatted_results),
            "search_type": search_type,
        }

    finally:
        if should_close:
            session.close()


def main():
    """Entry point for the MCP server."""
    try:
        mcp.run(transport="http", host="0.0.0.0", port=8000, stateless=True)
    finally:
        close_all_sessions()


if __name__ == "__main__":
    main()
