"""Health check API endpoint for monitoring service status."""

from datetime import UTC, datetime
from typing import Annotated

import httpx
import redis
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from shared.config.settings import settings
from shared.db.session import get_db_dependency
from shared.schemas.common import HealthCheckResponse, ServiceStatus

SessionDep = Annotated[Session, Depends(get_db_dependency)]

router = APIRouter(prefix="/health", tags=["health"])


def check_postgresql(session: Session) -> ServiceStatus:
    """Check PostgreSQL connection."""
    try:
        session.execute(text("SELECT 1"))
        return ServiceStatus(
            status="healthy", message="PostgreSQL connection successful"
        )
    except Exception as e:
        return ServiceStatus(
            status="unhealthy", message=f"PostgreSQL connection failed: {str(e)}"
        )


def check_redis() -> ServiceStatus:
    """Check Redis connection."""
    try:
        client = redis.from_url(settings.redis_url)
        client.ping()
        return ServiceStatus(status="healthy", message="Redis connection successful")
    except Exception as e:
        return ServiceStatus(
            status="unhealthy", message=f"Redis connection failed: {str(e)}"
        )


async def check_qdrant() -> ServiceStatus:
    """Check Qdrant connection."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.qdrant_url}/")
            if response.status_code == 200:
                return ServiceStatus(
                    status="healthy", message="Qdrant connection successful"
                )
            return ServiceStatus(
                status="unhealthy",
                message=f"Qdrant returned status {response.status_code}",
            )
    except Exception as e:
        return ServiceStatus(
            status="unhealthy", message=f"Qdrant connection failed: {str(e)}"
        )


async def check_ollama() -> ServiceStatus:
    """
    Check Ollama connection via Tailscale.

    Ollama runs outside Docker (on host or remote machine) connected via Tailscale.
    Health check verifies connectivity via /api/version endpoint.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.ollama_url}/api/version")
            if response.status_code == 200:
                version = response.json().get("version", "unknown")
                return ServiceStatus(
                    status="healthy",
                    message=f"Ollama connection successful (version: {version})",
                )
            return ServiceStatus(
                status="unhealthy",
                message=f"Ollama returned status {response.status_code}",
            )
    except Exception as e:
        return ServiceStatus(
            status="unhealthy", message=f"Ollama connection failed: {str(e)}"
        )


@router.get("", response_model=HealthCheckResponse)
async def health_check(session: SessionDep) -> dict:
    """
    Comprehensive health check for all services.

    Checks:
    - PostgreSQL: Database connection
    - Redis: Cache connection
    - Qdrant: Vector database connection
    - Ollama: LLM service connection via Tailscale
    """
    services = {
        "database": check_postgresql(session),
        "redis": check_redis(),
        "qdrant": await check_qdrant(),
        "ollama": await check_ollama(),
    }

    # Determine overall status
    all_healthy = all(service.status == "healthy" for service in services.values())
    overall_status = "healthy" if all_healthy else "unhealthy"

    return HealthCheckResponse(
        status=overall_status,
        timestamp=datetime.now(UTC),
        services=services,
    )
