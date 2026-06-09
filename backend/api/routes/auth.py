"""Authentication API endpoints for login and token management."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared.auth.jwt import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from shared.config.settings import settings
from shared.db.models import Organization, User
from shared.db.session import get_db_dependency
from shared.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from shared.utils.logging import get_logger

logger = get_logger(__name__)

SessionDep = Annotated[Session, Depends(get_db_dependency)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: UserLogin,
    session: SessionDep,
) -> dict:
    """
    Authenticate user and return JWT access token.

    Token expiration: 8 hours
    """
    # Find user by email
    user = session.execute(
        select(User).where(User.email == login_data.email)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active before verifying password
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token (8 hours expiration)
    access_token = create_access_token(
        user_id=str(user.id),
        email=user.email,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes
        * 60,  # Convert minutes to seconds
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current authenticated user information."""
    return current_user


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    session: SessionDep,
) -> User:
    """
    Register a new user and create personal organization.

    Side effects:
    - Creates personal organization (is_personal=TRUE)
    - Hashes password with bcrypt
    """
    logger.info(
        "User registration attempt",
        email=user_data.email,
        username=user_data.username,
    )

    # Check if email already exists
    existing_email = session.execute(
        select(User).where(User.email == user_data.email)
    ).scalar_one_or_none()

    if existing_email:
        logger.warning(
            "Registration failed: email already exists",
            email=user_data.email,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Check if username already exists
    existing_username = session.execute(
        select(User).where(User.username == user_data.username)
    ).scalar_one_or_none()

    if existing_username:
        logger.warning(
            "Registration failed: username already taken",
            username=user_data.username,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    # Hash password
    password_hash = get_password_hash(user_data.password)

    # Create user
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=password_hash,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create personal organization
    org = Organization(
        name=f"{user.username}'s Personal Space",
        slug=f"{user.username}-personal",
        is_personal=True,
        created_by=user.id,
    )
    session.add(org)
    session.commit()
    session.refresh(org)

    logger.info(
        "User registered successfully",
        user_id=str(user.id),
        username=user.username,
    )

    return user
