"""Add Cooking Historys model

Revision ID: 0d8a6abad003
Revises: cb27bfed2365
Create Date: 2025-03-07 17:06:20.606900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d8a6abad003'
down_revision: Union[str, None] = 'cb27bfed2365'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cooking_historys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('recipeId', sa.Integer(), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    sa.Column('updatedAt', sa.DateTime(), nullable=True, server_default=sa.func.now(), onupdate=sa.func.now()),
    sa.ForeignKeyConstraint(['recipeId'], ['recipes.id'], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cooking_historys_id'), 'cooking_historys', ['id'], unique=False)
    

def downgrade() -> None:
    op.drop_index(op.f('ix_cooking_historys_id'), table_name='cooking_historys')
    op.drop_table('cooking_historys')