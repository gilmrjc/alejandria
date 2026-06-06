"""add_slug_to_folder_question_proposal

Revision ID: c6a9490ff3a8
Revises: 9a166b9a6dd2
Create Date: 2026-06-04 21:04:46.508665

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c6a9490ff3a8"
down_revision: str | None = "9a166b9a6dd2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add slug column to folders table (nullable initially for existing data)
    op.add_column("folders", sa.Column("slug", sa.String(length=200), nullable=True))

    # Add slug column to questions table (nullable initially for existing data)
    op.add_column("questions", sa.Column("slug", sa.String(length=200), nullable=True))

    # Add slug column to proposals table (nullable initially for existing data)
    op.add_column("proposals", sa.Column("slug", sa.String(length=200), nullable=True))

    # Generate slugs for existing folders (simpler approach)
    op.execute("""
        UPDATE folders
        SET slug = 'folder-' || replace(id::text, '-', '')
        WHERE slug IS NULL
    """)

    # Generate slugs for existing questions (simpler approach)
    op.execute("""
        UPDATE questions
        SET slug = 'question-' || replace(id::text, '-', '')
        WHERE slug IS NULL
    """)

    # Generate slugs for existing proposals (simpler approach)
    op.execute("""
        UPDATE proposals
        SET slug = 'proposal-' || replace(id::text, '-', '')
        WHERE slug IS NULL
    """)

    # Make slug non-nullable
    op.alter_column("folders", "slug", nullable=False)
    op.alter_column("questions", "slug", nullable=False)
    op.alter_column("proposals", "slug", nullable=False)

    # Create unique index on slug
    op.create_index("ix_folders_slug", "folders", ["slug"], unique=True)
    op.create_index("ix_questions_slug", "questions", ["slug"], unique=True)
    op.create_index("ix_proposals_slug", "proposals", ["slug"], unique=True)


def downgrade() -> None:
    # Drop slug column from proposals table
    op.drop_index("ix_proposals_slug", table_name="proposals")
    op.drop_column("proposals", "slug")

    # Drop slug column from questions table
    op.drop_index("ix_questions_slug", table_name="questions")
    op.drop_column("questions", "slug")

    # Drop slug column from folders table
    op.drop_index("ix_folders_slug", table_name="folders")
    op.drop_column("folders", "slug")
