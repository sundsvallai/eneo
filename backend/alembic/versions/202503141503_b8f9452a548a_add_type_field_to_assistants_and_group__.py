# flake8: noqa

"""add_type_field_to_assistants_and_group_chats
Revision ID: b8f9452a548a
Revises: 360b00fa0466
Create Date: 2025-03-14 15:03:07.285693
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "b8f9452a548a"
down_revision = "360b00fa0466"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add type column to assistants table
    op.add_column("assistants", sa.Column("type", sa.String(), nullable=True))

    # Add type column to group_chats table
    op.add_column("group_chats", sa.Column("type", sa.String(), nullable=True))

    # Set default values for existing records
    # For assistants table: use 'default-assistant' for records where is_default=True, otherwise 'assistant'
    op.execute(
        "UPDATE assistants SET type = CASE WHEN is_default = TRUE THEN 'default-assistant' ELSE 'assistant' END"
    )
    op.execute("UPDATE group_chats SET type = 'group-chat'")

    # Make columns not nullable after setting defaults
    op.alter_column("assistants", "type", nullable=False)
    op.alter_column("group_chats", "type", nullable=False)


def downgrade() -> None:
    # Remove type column from assistants and group_chats tables
    op.drop_column("assistants", "type")
    op.drop_column("group_chats", "type")
