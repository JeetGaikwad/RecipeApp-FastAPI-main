"""Add Wishlists model

Revision ID: cb27bfed2365
Revises: b47ca81789e0
Create Date: 2025-03-07 17:05:21.750789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb27bfed2365'
down_revision: Union[str, None] = 'b47ca81789e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('wishlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('recipeId', sa.Integer(), nullable=False),
    sa.Column('visibility', sa.Enum('public', 'private', name='visiblityenum'), nullable=True, server_default='private'),
    sa.Column('createdAt', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    sa.Column('updatedAt', sa.DateTime(), nullable=True, server_default=sa.func.now(), onupdate=sa.func.now()),
    sa.ForeignKeyConstraint(['recipeId'], ['recipes.id'], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wishlists_id'), 'wishlists', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_wishlists_id'), table_name='wishlists')
    op.drop_table('wishlists')