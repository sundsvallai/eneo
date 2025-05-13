# flake8: noqa

"""add_transcription_model_id_to_apps
Revision ID: b821ca19d819
Revises: 82667b53d2b1
Create Date: 2025-03-11 14:54:53.180571
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic
revision = 'b821ca19d819'
down_revision = '82667b53d2b1'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add transcription_model_id column to Apps table
    op.add_column('apps', sa.Column('transcription_model_id', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Add foreign key constraint
    op.create_foreign_key(
        "fk_apps_transcription_models",
        "apps", "transcription_models",
        ["transcription_model_id"], ["id"],
        ondelete="SET NULL"
    )
    
    # Set the default transcription model (KB-Whisper) for all existing apps
    conn = op.get_bind()
    
    # Get KB-Whisper model ID
    kb_whisper = conn.execute(sa.text("SELECT id FROM transcription_models WHERE model_name = 'KBLab/kb-whisper-large'")).fetchone()
    
    if kb_whisper:
        kb_whisper_id = kb_whisper[0]
        
        # Update all existing apps to use KB-Whisper as the default transcription model
        conn.execute(
            sa.text("""
                UPDATE apps
                SET transcription_model_id = :model_id
            """),
            parameters={"model_id": kb_whisper_id}
        )

def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint("fk_apps_transcription_models", "apps", type_="foreignkey")
    
    # Drop column
    op.drop_column('apps', 'transcription_model_id')