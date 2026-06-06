"""User schemas for API request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern="^[a-zA-Z0-9_]+$",
        description="Username (alphanumeric + underscores)",
    )


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(
        ..., min_length=8, max_length=128, description="User password"
    )


class UserResponse(BaseModel):
    """Schema for user response."""

    id: UUID = Field(description="User ID")
    email: str = Field(description="User email address")
    username: str = Field(description="Username")
    is_active: bool = Field(description="User active status")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """Schema for JWT token response."""

    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(description="Token expiration time in seconds")
