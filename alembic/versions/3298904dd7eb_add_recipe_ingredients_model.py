"""Add Recipe Ingredients model

Revision ID: 3298904dd7eb
Revises: df043cfb7a9a
Create Date: 2025-03-07 17:01:58.885261

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3298904dd7eb"
down_revision: Union[str, None] = "df043cfb7a9a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ingredientName", sa.String(length=255), nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ingredients_id"), "ingredients", ["id"], unique=False)

    op.create_table(
        "recipe_ingredients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ingredientId", sa.Integer(), nullable=False),
        sa.Column("recipeId", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column(
            "unit",
            sa.Enum(
                "gram",
                "kilogram",
                "liter",
                "mililiter",
                "teaspoon",
                "tablespoon",
                "cup",
                "piece",
                name="weightunit",
            ),
            nullable=False,
        ),
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
        sa.ForeignKeyConstraint(
            ["ingredientId"], ["ingredients.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["recipeId"], ["recipes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_recipe_ingredients_id"), "recipe_ingredients", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_recipe_ingredients_id"), table_name="recipe_ingredients")
    op.drop_table("recipe_ingredients")

    op.drop_index(op.f("ix_ingredients_id"), table_name="ingredients")
    op.drop_table("ingredients")
