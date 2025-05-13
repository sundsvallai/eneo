"""add_base_url_to_completion_models

Revision ID: 22e39d7c9fa4
Revises: 8184cbc174ae
Create Date: 2025-03-04 10:19:20.979598

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '22e39d7c9fa4'
down_revision = '8184cbc174ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add base_url column to completion_models table
    op.add_column(
        'completion_models', sa.Column('base_url', sa.String(), nullable=True)
    )


def downgrade() -> None:
    # Remove base_url column from completion_models table
    op.drop_column('completion_models', 'base_url')
