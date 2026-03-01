"""add content column

Revision ID: 19bbcdff5adf
Revises: d5f60df5950a
Create Date: 2026-03-01 22:57:08.170944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19bbcdff5adf'
down_revision: Union[str, Sequence[str], None] = 'd5f60df5950a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
