# flake8: noqa

"""add_transcription_to_files
Revision ID: 360b00fa0466
Revises: d6e118655ff5
Create Date: 2025-03-13 13:28:17.140094
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TEXT


# revision identifiers, used by Alembic
revision = '360b00fa0466'
down_revision = 'd6e118655ff5'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # We use TEXT type instead of String to accommodate large transcription texts
    op.add_column('files', sa.Column('transcription', TEXT, nullable=True))

def downgrade() -> None:
    op.drop_column('files', 'transcription')