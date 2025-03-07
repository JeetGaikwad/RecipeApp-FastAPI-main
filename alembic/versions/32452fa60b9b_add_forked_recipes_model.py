"""Add Forked Recipes model

Revision ID: 32452fa60b9b
Revises: 0d8a6abad003
Create Date: 2025-03-07 17:07:30.038261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32452fa60b9b'
down_revision: Union[str, None] = '0d8a6abad003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('forked_recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('recipeId', sa.Integer(), nullable=False),
    sa.Column('recipeName', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('recipeType', sa.Enum('veg', 'nonveg', name='tag'), nullable=False),
    sa.Column('peopleCount', sa.Integer(), nullable=True, server_default=sa.text('1')),
    sa.Column('createdAt', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    sa.Column('updatedAt', sa.DateTime(), nullable=True, server_default=sa.func.now(), onupdate=sa.func.now()),
    sa.ForeignKeyConstraint(['recipeId'], ['recipes.id'], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forked_recipes_id'), 'forked_recipes', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_forked_recipes_id'), table_name='forked_recipes')
    op.drop_table('forked_recipes')
