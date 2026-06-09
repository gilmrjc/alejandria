"""Database session management."""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..config.settings import settings
from .models import Base

# Global engine and session maker (singleton pattern)
_engine = None
_session_maker = None


def get_engine(database_url: str = None):
    """Create database engine with connection pooling (singleton)."""
    global _engine
    if _engine is None:
        if database_url is None:
            database_url = settings.database_url

        _engine = create_engine(
            database_url,
            echo=settings.debug,
            pool_size=10,  # Number of connections to keep in pool
            max_overflow=20,  # Max additional connections beyond pool_size
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_timeout=30,  # Timeout for getting connection from pool
        )
    return _engine


def get_session_maker(engine=None):
    """Get session maker bound to engine (singleton)."""
    global _session_maker
    if _session_maker is None:
        if engine is None:
            engine = get_engine()
        _session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _session_maker


def get_db_session() -> Session:
    """Get a new database session."""
    return get_session_maker()()


def get_db_dependency():
    """Dependency for FastAPI - yields session with automatic cleanup."""
    session = get_db_session()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def get_db_session_context():
    """Context manager for database session with automatic cleanup."""
    session = get_db_session()
    try:
        yield session
    finally:
        session.close()


def init_db(engine=None):
    """Initialize database tables."""
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(bind=engine)
