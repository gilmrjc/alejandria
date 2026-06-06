"""Database session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..config.settings import settings
from .models import Base


def get_engine(database_url: str = None):
    """Create database engine with connection pooling."""
    if database_url is None:
        database_url = settings.database_url

    return create_engine(
        database_url,
        echo=settings.debug,
        pool_size=10,  # Number of connections to keep in pool
        max_overflow=20,  # Max additional connections beyond pool_size
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,  # Recycle connections after 1 hour
        pool_timeout=30,  # Timeout for getting connection from pool
    )


def get_session_maker(engine=None):
    """Get session maker bound to engine."""
    if engine is None:
        engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    """Get a new database session."""
    session_local = get_session_maker()
    return session_local()


def init_db(engine=None):
    """Initialize database tables."""
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(bind=engine)
