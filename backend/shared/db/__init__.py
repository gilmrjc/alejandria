"""Database module for Alejandria."""

# Import middleware to register event listeners
from . import middleware  # noqa: F401, I001 - Import has side effects: registers SQLAlchemy event listeners
from .models import (
    Base,
    Document,
    DocumentRelationship,
    DocumentSnapshot,
    Folder,
    Gap,
    GapTag,
    Job,
    Organization,
    Project,
    Proposal,
    ProposalDocument,
    ProposalGap,
    QdrantCollection,
    Question,
    QuestionDocumentReference,
    QuestionGapReference,
    Tag,
    User,
    VectorSyncLog,
)
from .session import get_db_session, init_db

__all__ = [
    "Base",
    "Document",
    "DocumentRelationship",
    "DocumentSnapshot",
    "Folder",
    "Gap",
    "GapTag",
    "Job",
    "Organization",
    "Project",
    "Proposal",
    "ProposalDocument",
    "ProposalGap",
    "QdrantCollection",
    "Question",
    "QuestionDocumentReference",
    "QuestionGapReference",
    "Tag",
    "User",
    "VectorSyncLog",
    "get_db_session",
    "init_db",
]
