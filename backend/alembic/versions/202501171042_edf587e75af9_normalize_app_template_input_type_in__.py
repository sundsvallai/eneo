"""Normalize App template input type in database
Revision ID: edf587e75af9
Revises: e748bf9c8b1d
Create Date: 2025-01-17 10:42:40.051220
"""

from alembic import op

# revision identifiers, used by Alembic
revision = "edf587e75af9"
down_revision = "e748bf9c8b1d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE app_templates
        SET input_type = 'text-field'
        WHERE input_type = 'Text Document';
    """
    )

    op.execute(
        """
        UPDATE app_templates
        SET input_type = 'audio-recorder'
        WHERE input_type = 'Record Voice';
    """
    )

    op.execute(
        """
        UPDATE app_templates
        SET input_type = 'image-upload'
        WHERE input_type = 'Picture';
    """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE app_templates
        SET input_type = 'Text Document'
        WHERE input_type = 'text-field';
    """
    )

    op.execute(
        """
        UPDATE app_templates
        SET input_type = 'Record Voice'
        WHERE input_type = 'audio-recorder';
    """
    )

    op.execute(
        """
        UPDATE app_templates
        SET input_type = 'Picture'
        WHERE input_type = 'image-upload';
    """
    )
