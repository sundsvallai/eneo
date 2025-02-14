"""rename preferred -> default
Revision ID: eb2ae95163b6
Revises: c5ab99259246
Create Date: 2025-02-03 12:51:00.907282
"""

from alembic import op

# revision identifiers, used by Alembic
revision = 'eb2ae95163b6'
down_revision = 'c5ab99259246'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Adjusted commands to use rename instead of drop/add ###
    op.alter_column(
        'completion_model_settings',
        'is_org_preferred',
        new_column_name='is_org_default',
    )

    op.alter_column(
        'embedding_model_settings', 'is_org_preferred', new_column_name='is_org_default'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### Adjusted commands to use rename instead of add/drop ###
    op.alter_column(
        'embedding_model_settings', 'is_org_default', new_column_name='is_org_preferred'
    )

    op.alter_column(
        'completion_model_settings',
        'is_org_default',
        new_column_name='is_org_preferred',
    )
    # ### end Alembic commands ###
