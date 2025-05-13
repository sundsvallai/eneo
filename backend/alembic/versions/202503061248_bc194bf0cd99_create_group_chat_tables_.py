"""create group chat tables
Revision ID: bc194bf0cd99
Revises: 797fdf35cf81
Create Date: 2025-02-25 11:31:22.751471
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "bc194bf0cd99"
down_revision = "797fdf35cf81"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the GroupChats table
    op.create_table(
        "group_chats",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("allow_mentions", sa.Boolean(), default=False),
        sa.Column("show_response_label", sa.Boolean(), default=False),
        sa.Column("published", sa.Boolean(), default=False),
        sa.Column("space_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["space_id"], ["spaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create the GroupChatsAssistantsMapping table
    op.create_table(
        "group_chats_assistants_mapping",
        sa.Column("group_chat_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("assistant_id", sa.UUID(), nullable=False),
        sa.Column("user_description", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["group_chat_id"], ["group_chats.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["assistant_id"], ["assistants.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("group_chat_id", "assistant_id"),
    )


def downgrade() -> None:
    # Drop the GroupChatsAssistantsMapping table first due to foreign key constraints
    op.drop_table("group_chats_assistants_mapping")
    op.drop_table("group_chats")
