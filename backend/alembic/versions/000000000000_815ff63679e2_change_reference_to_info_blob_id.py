"""change reference to info_blob_id
Revision ID: 815ff63679e2
Revises: 2757a8c54d1b
Create Date: 2023-05-15 20:59:21.982017
"""

from alembic import op

# revision identifiers, used by Alembic
revision = "815ff63679e2"
down_revision = "2757a8c54d1b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "info_blob_references",
        "reference",
        nullable=False,
        new_column_name="info_blob_id",
    )


def downgrade() -> None:
    op.alter_column(
        "info_blob_references",
        "info_blob_id",
        nullable=False,
        new_column_name="reference",
    )
