# flake8: noqa

"""add_spaces_transcription_models
Revision ID: 82667b53d2b1
Revises: 65ff84b31e90
Create Date: 2025-03-11 12:32:18.765169
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = '82667b53d2b1'
down_revision = '65ff84b31e90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create spaces_transcription_models junction table
    op.create_table(
        'spaces_transcription_models',
        sa.Column('space_id', sa.UUID(), nullable=False),
        sa.Column('transcription_model_id', sa.UUID(), nullable=False),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['space_id'], ['spaces.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['transcription_model_id'], ['transcription_models.id'], ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('space_id', 'transcription_model_id'),
    )

    # Add the default transcription model (KB-Whisper) to all non-personal spaces
    conn = op.get_bind()

    # Get KB-Whisper model ID
    kb_whisper = conn.execute(
        sa.text(
            "SELECT id FROM transcription_models WHERE model_name = 'KBLab/kb-whisper-large'"
        )
    ).fetchone()

    if kb_whisper:
        kb_whisper_id = kb_whisper[0]

        # Get all non-personal spaces (where user_id IS NULL)
        spaces = conn.execute(
            sa.text("SELECT id FROM spaces WHERE user_id IS NULL")
        ).fetchall()

        # Associate KB-Whisper model with each non-personal space
        for space in spaces:
            conn.execute(
                sa.text(
                    """
                    INSERT INTO spaces_transcription_models
                    (space_id, transcription_model_id)
                    VALUES (:space_id, :model_id)
                """
                ),
                parameters={"space_id": space[0], "model_id": kb_whisper_id},
            )


def downgrade() -> None:
    op.drop_table('spaces_transcription_models')
