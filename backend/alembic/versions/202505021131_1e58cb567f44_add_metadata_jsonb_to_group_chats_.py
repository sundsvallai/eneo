# flake8: noqa

"""add_metadata_jsonb_to_group_chats
Revision ID: 1e58cb567f44
Revises: cf0d116542e5
Create Date: 2025-05-02 11:31:19.609655
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic
revision = "1e58cb567f44"
down_revision = "cf0d116542e5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("group_chats", sa.Column("metadata_json", JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column("group_chats", "metadata_json")
