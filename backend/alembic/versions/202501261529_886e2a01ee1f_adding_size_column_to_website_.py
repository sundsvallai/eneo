"""adding size column to website
Revision ID: 886e2a01ee1f
Revises: 77ec960315a1
Create Date: 2025-01-24 15:29:48.673988
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "886e2a01ee1f"
down_revision = "77ec960315a1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("websites", sa.Column("size", sa.BigInteger(), nullable=True))

    op.execute(
        """
        UPDATE websites
        SET size = (
            SELECT COALESCE(SUM(size), 0)
            FROM info_blobs
            WHERE info_blobs.website_id = websites.id
            )
        """
    )

    op.alter_column("websites", "size", nullable=False)


def downgrade() -> None:
    op.drop_column("websites", "size")
