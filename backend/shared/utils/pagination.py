"""Pagination utilities for API endpoints."""

from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session


def apply_pagination(
    query: Select,
    session: Session,
    page: int = 1,
    per_page: int = 25,
) -> tuple[list[Any], int, int]:
    """
    Apply pagination to a SQLAlchemy query.

    Args:
        query: SQLAlchemy select query
        session: Database session
        page: Page number (starting from 1)
        per_page: Items per page

    Returns:
        Tuple of (items, total, total_pages)
    """
    # Get total count - use subquery approach for SQLAlchemy 2.0
    count_query = select(func.count()).select_from(query.subquery())
    total = session.scalar(count_query) or 0

    # Apply pagination
    offset = (page - 1) * per_page
    paginated_query = query.offset(offset).limit(per_page)

    items = session.execute(paginated_query).scalars().all()

    # Calculate total pages
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return list(items), total, total_pages


def build_pagination_response(
    items: list[Any],
    page: int,
    per_page: int,
    total: int,
    total_pages: int,
) -> dict:
    """
    Build a standardized pagination response.

    Args:
        items: List of items
        page: Current page number
        per_page: Items per page
        total: Total number of items
        total_pages: Total number of pages

    Returns:
        Dictionary with items and pagination metadata
    """
    return {
        "items": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        },
    }
