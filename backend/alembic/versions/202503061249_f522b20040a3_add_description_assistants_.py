"""add_description_assistants
Revision ID: f522b20040a3
Revises: bc194bf0cd99
Create Date: 2025-03-04 15:19:04.397763
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "f522b20040a3"
down_revision = "bc194bf0cd99"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add column to assistants
    op.add_column("assistants", sa.Column("description", sa.String, nullable=True))


def downgrade() -> None:
    # drop the column
    op.drop_column("assistants", "description")
