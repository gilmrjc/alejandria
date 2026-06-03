"""Database module for Alejandria."""

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

# Import middleware to register event listeners
from . import middleware

__all__ = [
    'Base',
    'Document',
    'DocumentRelationship',
    'DocumentSnapshot',
    'Folder',
    'Gap',
    'GapTag',
    'Job',
    'Organization',
    'Project',
    'Proposal',
    'ProposalDocument',
    'ProposalGap',
    'QdrantCollection',
    'Question',
    'QuestionDocumentReference',
    'QuestionGapReference',
    'Tag',
    'User',
    'VectorSyncLog',
    'get_db_session',
    'init_db',
]
