"""add col chat_model_prompt to settings
Revision ID: d8f7c2465854
Revises: e93839166d18
Create Date: 2023-06-07 00:01:23.293859
"""

from alembic import op
import sqlalchemy as sa


SETTINGS_TABLE_NAME = "settings"

# revision identifiers, used by Alembic
revision = "d8f7c2465854"
down_revision = "e93839166d18"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add column to settings
    op.add_column(
        SETTINGS_TABLE_NAME,
        sa.Column(
            "chat_model_prompt",
            sa.Text,
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(SETTINGS_TABLE_NAME, "chat_model_prompt")
