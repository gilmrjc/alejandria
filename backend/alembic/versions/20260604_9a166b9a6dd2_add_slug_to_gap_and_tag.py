"""add_slug_to_gap_and_tag

Revision ID: 9a166b9a6dd2
Revises: 071e1eea8aaa
Create Date: 2026-06-04 20:52:09.215310

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9a166b9a6dd2"
down_revision: str | None = "071e1eea8aaa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add slug column to gaps table (nullable initially for existing data)
    op.add_column("gaps", sa.Column("slug", sa.String(length=200), nullable=True))

    # Add slug column to tags table (nullable initially for existing data)
    op.add_column("tags", sa.Column("slug", sa.String(length=200), nullable=True))

    # Generate slugs for existing gaps (simpler approach)
    op.execute("""
        UPDATE gaps
        SET slug = 'gap-' || replace(id::text, '-', '')
        WHERE slug IS NULL
    """)

    # Generate slugs for existing tags (simpler approach)
    op.execute("""
        UPDATE tags
        SET slug = 'tag-' || replace(id::text, '-', '')
        WHERE slug IS NULL
    """)

    # Make slug non-nullable
    op.alter_column("gaps", "slug", nullable=False)
    op.alter_column("tags", "slug", nullable=False)

    # Create unique index on slug
    op.create_index("ix_gaps_slug", "gaps", ["slug"], unique=True)
    op.create_index("ix_tags_slug", "tags", ["slug"], unique=True)


def downgrade() -> None:
    # Drop slug column from tags table
    op.drop_index("ix_tags_slug", table_name="tags")
    op.drop_column("tags", "slug")

    # Drop slug column from gaps table
    op.drop_index("ix_gaps_slug", table_name="gaps")
    op.drop_column("gaps", "slug")
