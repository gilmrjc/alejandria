"""Unit tests for error handler middleware."""

from fastapi import FastAPI

from api.middleware.error_handler import setup_error_handling


def test_error_handler_setup():
    """Test that error handler is set up correctly."""
    app = FastAPI()
    setup_error_handling(app)

    # Check that exception handler was added
    assert Exception in app.exception_handlers


def test_error_response_structure():
    """Test that ErrorResponse structure works correctly."""
    from api.middleware.error_handler import ErrorResponse

    error = ErrorResponse(
        message="Test error",
        error_code="TEST_ERROR",
        details={"key": "value"},
        request_id="test-123",
    )

    result = error.to_dict()
    assert result["message"] == "Test error"
    assert result["error_code"] == "TEST_ERROR"
    assert result["details"] == {"key": "value"}
    assert result["request_id"] == "test-123"


def test_error_response_without_details():
    """Test that ErrorResponse works without details."""
    from api.middleware.error_handler import ErrorResponse

    error = ErrorResponse(
        message="Test error",
        error_code="TEST_ERROR",
    )

    result = error.to_dict()
    assert result["message"] == "Test error"
    assert result["error_code"] == "TEST_ERROR"
    assert "details" not in result
    assert "request_id" not in result


def test_error_response_default_error_code():
    """Test that ErrorResponse uses default error code."""
    from api.middleware.error_handler import ErrorResponse

    error = ErrorResponse(message="Test error")

    result = error.to_dict()
    assert result["message"] == "Test error"
    assert result["error_code"] == "INTERNAL_ERROR"
