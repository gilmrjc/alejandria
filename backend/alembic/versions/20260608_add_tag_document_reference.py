"""add_gap_document_reference

Revision ID: add_gap_document_reference
Revises: 78fca62ad0f2
Create Date: 2026-06-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'add_gap_document_reference'
down_revision: Union[str, None] = '78fca62ad0f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'gap_document_references',
        sa.Column('gap_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['gap_id'], ['gaps.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['document_id'], ['documents.id'], ondelete='CASCADE'
        )
    )


def downgrade() -> None:
    op.drop_table('gap_document_references')
