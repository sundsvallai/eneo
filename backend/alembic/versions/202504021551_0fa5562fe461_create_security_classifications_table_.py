# flake8: noqa

"""create_security_classifications_table
Revision ID: 0fa5562fe461
Revises: e3577e247d59
Create Date: 2025-03-27 11:51:24.270062
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "0fa5562fe461"
down_revision = "e3577e247d59"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create security levels table
    op.create_table(
        "security_classifications",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("security_level", sa.Integer(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "tenant_id"),
    )

    # Add security level reference to spaces table
    op.add_column(
        "spaces",
        sa.Column(
            "security_classification_id",
            sa.UUID(),
            sa.ForeignKey("security_classifications.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    # Add security level reference to completion model settings table
    op.add_column(
        "completion_model_settings",
        sa.Column(
            "security_classification_id",
            sa.UUID(),
            sa.ForeignKey("security_classifications.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    # Add security level reference to embedding model settings table
    op.add_column(
        "embedding_model_settings",
        sa.Column(
            "security_classification_id",
            sa.UUID(),
            sa.ForeignKey("security_classifications.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    # Add security level reference to transcription model settings table
    op.add_column(
        "transcription_model_settings",
        sa.Column(
            "security_classification_id",
            sa.UUID(),
            sa.ForeignKey("security_classifications.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    # Remove security level references
    op.drop_column("transcription_model_settings", "security_classification_id")
    op.drop_column("embedding_model_settings", "security_classification_id")
    op.drop_column("completion_model_settings", "security_classification_id")
    op.drop_column("spaces", "security_classification_id")

    # Drop security levels table
    op.drop_table("security_classifications")
