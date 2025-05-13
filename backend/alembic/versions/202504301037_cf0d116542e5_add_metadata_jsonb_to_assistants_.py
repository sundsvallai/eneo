# flake8: noqa

"""add_metadata_jsonb_to_assistants
Revision ID: cf0d116542e5
Revises: 044f3350ffb8
Create Date: 2025-04-30 10:37:53.961985
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic
revision = "cf0d116542e5"
down_revision = "044f3350ffb8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("assistants", sa.Column("metadata_json", JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column("assistants", "metadata_json")
