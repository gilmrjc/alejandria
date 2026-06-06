"""Standardized error handling middleware for FastAPI."""

import uuid

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from shared.utils.logging import get_logger

logger = get_logger(__name__)


class ErrorResponse:
    """Standard error response structure."""

    def __init__(
        self,
        message: str,
        error_code: str = None,
        details: dict = None,
        request_id: str = None,
    ):
        self.message = message
        self.error_code = error_code or "INTERNAL_ERROR"
        self.details = details or {}
        self.request_id = request_id

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON response."""
        response = {
            "message": self.message,
            "error_code": self.error_code,
        }
        if self.details:
            response["details"] = self.details
        if self.request_id:
            response["request_id"] = self.request_id
        return response


async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global error handler for all exceptions.

    Args:
        request: FastAPI request
        exc: Exception that was raised

    Returns:
        JSONResponse with standardized error format
    """
    request_id = str(uuid.uuid4())

    # Log the error with request context
    logger.error(
        f"Request failed: {request.method} {request.url.path}",
        extra={
            "request_id": request_id,
            "exception": str(exc),
            "exception_type": type(exc).__name__,
        },
    )

    # Handle different exception types
    if isinstance(exc, HTTPException):
        return await handle_http_exception(exc, request_id)
    elif isinstance(exc, ValidationError):
        return await handle_validation_error(exc, request_id)
    elif isinstance(exc, SQLAlchemyError):
        return await handle_database_error(exc, request_id)
    else:
        return await handle_generic_error(exc, request_id)


async def handle_http_exception(exc: HTTPException, request_id: str) -> JSONResponse:
    """Handle HTTP exceptions from FastAPI."""
    error_response = ErrorResponse(
        message=exc.detail,
        error_code=f"HTTP_{exc.status_code}",
        request_id=request_id,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.to_dict(),
    )


async def handle_validation_error(
    exc: ValidationError, request_id: str
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    error_details = []
    for error in exc.errors():
        error_details.append(
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    error_response = ErrorResponse(
        message="Validation failed",
        error_code="VALIDATION_ERROR",
        details={"errors": error_details},
        request_id=request_id,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.to_dict(),
    )


async def handle_database_error(exc: SQLAlchemyError, request_id: str) -> JSONResponse:
    """Handle SQLAlchemy database errors."""
    error_response = ErrorResponse(
        message="Database operation failed",
        error_code="DATABASE_ERROR",
        request_id=request_id,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.to_dict(),
    )


async def handle_generic_error(exc: Exception, request_id: str) -> JSONResponse:
    """Handle all other exceptions."""
    error_response = ErrorResponse(
        message="An unexpected error occurred",
        error_code="INTERNAL_ERROR",
        request_id=request_id,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.to_dict(),
    )


def setup_error_handling(app):
    """
    Set up error handling middleware for the FastAPI app.

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(Exception, error_handler)
