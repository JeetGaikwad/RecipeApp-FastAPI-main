"""Add Follows model

Revision ID: 1bab2dbb3ab6
Revises: 3298904dd7eb
Create Date: 2025-03-07 17:02:59.277980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bab2dbb3ab6'
down_revision: Union[str, None] = '3298904dd7eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('follows',
    sa.Column('followerId', sa.Integer(), nullable=False),
    sa.Column('followeeId', sa.Integer(), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    sa.ForeignKeyConstraint(['followeeId'], ['users.id'], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(['followerId'], ['users.id'], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint('followerId', 'followeeId')
    )


def downgrade() -> None:
    op.drop_table('follows')