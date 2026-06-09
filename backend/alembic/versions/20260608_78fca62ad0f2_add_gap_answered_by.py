"""add_gap_answered_by

Revision ID: 78fca62ad0f2
Revises: c6a9490ff3a8
Create Date: 2026-06-08 18:09:24.257265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78fca62ad0f2'
down_revision: Union[str, None] = 'c6a9490ff3a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('gaps', sa.Column('answered_by', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'fk_gaps_answered_by_users', 'gaps', 'users', ['answered_by'], ['id'], ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_constraint('fk_gaps_answered_by_users', 'gaps', type_='foreignkey')
    op.drop_column('gaps', 'answered_by')
