"""Database session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base  # noqa: F401
from .models import (
    User,
    Organization,
    Project,
    Folder,
    Document,
    DocumentRelationship,
    Gap,
    Tag,
    GapTag,
    Question,
    QuestionDocumentReference,
    QuestionGapReference,
    Proposal,
    ProposalDocument,
    ProposalGap,
    DocumentSnapshot,
    VectorSyncLog,
    Job,
    QdrantCollection,
)
from ..config.settings import settings


def get_engine(database_url: str = None):
    """Create database engine."""
    if database_url is None:
        database_url = settings.database_url

    return create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
    )


def get_session_maker(engine=None):
    """Get session maker bound to engine."""
    if engine is None:
        engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    """Get a new database session."""
    SessionLocal = get_session_maker()
    return SessionLocal()


def init_db(engine=None):
    """Initialize database tables."""
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(bind=engine)
