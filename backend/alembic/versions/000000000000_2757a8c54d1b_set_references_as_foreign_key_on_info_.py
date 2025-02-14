"""set references as foreign key on info_blobs
Revision ID: 2757a8c54d1b
Revises: a244a4aa2d8c
Create Date: 2023-05-15 17:58:57.549756
"""

from alembic import op

# revision identifiers, used by Alembic
revision = "2757a8c54d1b"
down_revision = "a244a4aa2d8c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        constraint_name="info_blob_references_reference_fkey",
        source_table="info_blob_references",
        referent_table="info_blobs",
        local_cols=["reference"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        constraint_name="info_blob_references_reference_fkey",
        table_name="info_blob_references",
    )
