"""Add User model

Revision ID: 6761fb7e5a54
Revises:
Create Date: 2025-03-07 15:44:05.301184

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6761fb7e5a54"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("firstName", sa.String(length=255), nullable=True),
        sa.Column("lastName", sa.String(length=255), nullable=True),
        sa.Column("bio", sa.String(length=500), nullable=True),
        sa.Column("profilePhoto", sa.String(length=255), nullable=True),
        sa.Column("dateOfBirth", sa.DateTime(), nullable=True),
        sa.Column("phoneNumber", sa.String(length=30), nullable=True),
        sa.Column("password", sa.String(length=300), nullable=False),
        sa.Column("role", sa.Enum("admin", "user", name="userrole"), nullable=False),
        sa.Column(
            "followersCount", sa.Integer(), nullable=True, server_default=sa.text("0")
        ),
        sa.Column(
            "followingCount", sa.Integer(), nullable=True, server_default=sa.text("0")
        ),
        sa.Column("isBlocked", sa.Boolean(), nullable=True),
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
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
