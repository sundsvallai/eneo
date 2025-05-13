# flake8: noqa

"""add_security_classification_enable_column_to_tenant
Revision ID: f8b7664ea8aa
Revises: 0fa5562fe461
Create Date: 2025-04-03 10:42:22.858352
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = "f8b7664ea8aa"
down_revision = "0fa5562fe461"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add security_enabled column to tenants table
    op.add_column(
        "tenants",
        sa.Column(
            "security_enabled", sa.Boolean(), server_default="false", nullable=False
        ),
    )


def downgrade() -> None:
    # Drop security_enabled column from tenants table
    op.drop_column("tenants", "security_enabled")
