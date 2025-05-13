# flake8: noqa

"""add_swe_hosting_module
Revision ID: e3577e247d59
Revises: 7158f416e35c
Create Date: 2025-04-02 15:33:34.658573
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic
revision = 'e3577e247d59'
down_revision = '7158f416e35c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if the module already exists to avoid duplicates
    conn = op.get_bind()
    result = conn.execute(text("SELECT id FROM modules WHERE name = 'SWE Models'"))
    if result.fetchone() is None:
        conn.execute(text("INSERT INTO modules (name) VALUES ('SWE Models')"))


def downgrade() -> None:
    # Remove the module if needed
    conn = op.get_bind()
    conn.execute(text("DELETE FROM modules WHERE name = 'SWE Models'"))
