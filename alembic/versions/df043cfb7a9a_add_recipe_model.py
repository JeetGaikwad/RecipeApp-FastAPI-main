"""Add Recipe model

Revision ID: df043cfb7a9a
Revises: 6761fb7e5a54
Create Date: 2025-03-07 17:00:06.105275

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "df043cfb7a9a"
down_revision: Union[str, None] = "6761fb7e5a54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("userId", sa.Integer(), nullable=False),
        sa.Column("recipeName", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("recipeType", sa.Enum("veg", "nonveg", name="tag"), nullable=False),
        sa.Column(
            "peopleCount", sa.Integer(), nullable=True, server_default=sa.text("1")
        ),
        sa.Column(
            "likesCount", sa.Integer(), nullable=True, server_default=sa.text("0")
        ),
        sa.Column(
            "forkedCount", sa.Integer(), nullable=True, server_default=sa.text("0")
        ),
        sa.Column(
            "isDeleted", sa.Boolean(), nullable=True, server_default=sa.text("0")
        ),
        sa.Column("isHide", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column(
            "createdAt", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updatedAt",
            sa.DateTime(),
            nullable=True,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.Column("deletedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["userId"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recipes_id"), "recipes", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_recipes_id"), table_name="recipes")
    op.drop_table("recipes")
