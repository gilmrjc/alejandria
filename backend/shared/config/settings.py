"""
Configuration management using Pydantic Settings.

This module provides type-safe configuration management for the application,
loading values from environment variables with sensible defaults.
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_env: str = Field(description="Application environment")
    debug: bool = Field(description="Debug mode")
    log_level: str = Field(description="Logging level")

    # Security
    secret_key: str | None = Field(
        default=None,
        description="Secret key for JWT token generation (required in production)",
    )
    algorithm: str = Field(description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        description="Access token expiration time in minutes"
    )

    # Database
    database_url: str = Field(description="PostgreSQL database URL")
    test_database_url: str | None = Field(
        default=None, description="PostgreSQL test database URL"
    )

    # Redis
    redis_url: str = Field(description="Redis connection URL")

    # Qdrant
    qdrant_url: str = Field(description="Qdrant HTTP API URL")
    qdrant_grpc_url: str = Field(description="Qdrant gRPC URL")

    # Ollama
    ollama_url: str = Field(description="Ollama API URL for LLM embeddings")

    # Celery-Once configuration (required by celery_once library)
    ONCE: dict = Field(
        default={
            "backend": "celery_once.backends.redis.Redis",
            "settings": {"url": "redis://localhost:6379/0"},
        },
        description="Celery-Once configuration for distributed task locks",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is a valid Python logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()

    @field_validator("app_env")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        """Validate application environment."""
        valid_envs = ["development", "staging", "production"]
        if v.lower() not in valid_envs:
            raise ValueError(f"app_env must be one of {valid_envs}")
        return v.lower()

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str | None, info) -> str:
        """Validate secret key is provided in production."""
        if info.data.get("app_env") == "production" and v is None:
            raise ValueError("SECRET_KEY must be set in production environment")
        if v is None:
            # Generate a random key for development
            import secrets

            return secrets.token_urlsafe(32)
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export settings instance for easy import
settings = get_settings()
