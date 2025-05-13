# flake8: noqa

"""add boolean column insight to assistants and group chats
Revision ID: ff2f32a493f2
Revises: b127c46c7ebc
Create Date: 2025-03-18 09:59:05.797683
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "ff2f32a493f2"
down_revision = "b127c46c7ebc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "assistants",
        sa.Column("insight_enabled", sa.Boolean(), default=False, nullable=True),
    )
    op.add_column(
        "group_chats",
        sa.Column("insight_enabled", sa.Boolean(), default=False, nullable=True),
    )

    op.execute("UPDATE group_chats SET insight_enabled = False")
    op.execute("UPDATE assistants SET insight_enabled = False")

    op.alter_column(
        "assistants",
        "insight_enabled",
        existing_type=sa.Boolean(),
        nullable=False,
    )

    op.alter_column(
        "group_chats",
        "insight_enabled",
        existing_type=sa.Boolean(),
        nullable=False,
    )


def downgrade() -> None:
    # First make the columns nullable before dropping them
    op.alter_column(
        "assistants",
        "insight_enabled",
        existing_type=sa.Boolean(),
        nullable=True,
    )

    op.alter_column(
        "group_chats",
        "insight_enabled",
        existing_type=sa.Boolean(),
        nullable=True,
    )

    # Now drop the columns
    op.drop_column("assistants", "insight_enabled")
    op.drop_column("group_chats", "insight_enabled")
