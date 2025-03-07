"""Add Recipe Likes model

Revision ID: 7ae7e09dfb99
Revises: 1bab2dbb3ab6
Create Date: 2025-03-07 17:03:52.039366

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7ae7e09dfb99"
down_revision: Union[str, None] = "1bab2dbb3ab6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "recipe_likes",
        sa.Column("userId", sa.Integer(), nullable=False),
        sa.Column("recipeId", sa.Integer(), nullable=False),
        sa.Column(
            "createdAt", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(["recipeId"], ["recipes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["userId"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("userId", "recipeId"),
    )


def downgrade() -> None:
    op.drop_table("recipe_likes")
