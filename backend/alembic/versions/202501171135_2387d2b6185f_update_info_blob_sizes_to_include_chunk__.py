"""update info_blob sizes to include chunk size sum; increase quota limit 10x.
Revision ID: 2387d2b6185f
Revises: edf587e75af9
Create Date: 2025-01-16 11:35:07.623888
"""

from alembic import op

# revision identifiers, used by Alembic
revision = "2387d2b6185f"
down_revision = "edf587e75af9"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.execute(
        """
        UPDATE info_blobs
        SET size = size + (
            SELECT COALESCE(SUM(size), 0)
            FROM info_blob_chunks
            WHERE info_blob_chunks.info_blob_id = info_blobs.id
        )
        """
    )

    op.execute(
        """
        UPDATE tenants
        SET quota_limit = quota_limit * 10
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE info_blobs
        SET size = OCTET_LENGTH(text)
        """
    )

    op.execute(
        """
        UPDATE tenants
        SET quota_limit = quota_limit / 10
        """
    )
