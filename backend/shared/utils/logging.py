"""Structured logging configuration using structlog."""

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict

from shared.config.settings import settings


def add_request_id(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add request ID to log events if available."""
    if "request_id" in event_dict:
        event_dict["request_id"] = event_dict["request_id"]
    return event_dict


def drop_color_message_key(
    logger: Any, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Drop the color_message key to avoid clutter in logs.

    This is useful when using structlog with standard logging handlers.
    """
    event_dict.pop("color_message", None)
    return event_dict


def configure_logging():
    """
    Configure structlog for the application.

    Sets up:
    - JSON output for production
    - Console output for development
    - Request ID tracking
    - Standard log levels
    """
    # Configure standard logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=settings.log_level,
    )

    # Shared processors for all configurations
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.app_env == "production":
        # Production: JSON output
        structlog.configure(
            processors=[
                *shared_processors,
                add_request_id,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(settings.log_level),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Development: Console output with colors
        structlog.configure(
            processors=[
                *shared_processors,
                add_request_id,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(settings.log_level),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger for a module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)
