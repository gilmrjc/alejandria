"""Pydantic schemas for API request/response validation."""

from .common import (
    HealthCheckResponse,
    PaginatedResponse,
    PaginationParams,
    ServiceStatus,
)
from .document import (
    DocumentCreate,
    DocumentListResponse,
    DocumentResponse,
    DocumentUpdate,
)
from .gap import (
    GapCreate,
    GapListResponse,
    GapResponse,
    GapUpdate,
)
from .user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)

__all__ = [
    # Document schemas
    "DocumentCreate",
    "DocumentUpdate",
    "DocumentResponse",
    "DocumentListResponse",
    # Gap schemas
    "GapCreate",
    "GapUpdate",
    "GapResponse",
    "GapListResponse",
    # User schemas
    "UserCreate",
    "UserResponse",
    "UserLogin",
    "TokenResponse",
    # Common schemas
    "PaginationParams",
    "PaginatedResponse",
    "HealthCheckResponse",
    "ServiceStatus",
]
