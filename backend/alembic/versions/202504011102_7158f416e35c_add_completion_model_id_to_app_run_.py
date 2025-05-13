# flake8: noqa

"""add_completion_model_id_to_app_run
Revision ID: 7158f416e35c
Revises: da3ec8750c0a
Create Date: 2025-04-01 11:02:33.858765
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '7158f416e35c'
down_revision = 'da3ec8750c0a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # First add the column as nullable
    op.add_column(
        'app_runs',
        sa.Column('completion_model_id', postgresql.UUID(as_uuid=True), nullable=True),
    )

    # Set completion_model_id from the parent app's completion_model_id for existing rows
    op.execute(
        """
        UPDATE app_runs 
        SET completion_model_id = apps.completion_model_id 
        FROM apps 
        WHERE app_runs.app_id = apps.id
    """
    )

    # Then make it non-nullable
    op.alter_column('app_runs', 'completion_model_id', nullable=False)

    # Add foreign key constraint
    op.create_foreign_key(
        "fk_app_runs_completion_model_id",
        "app_runs",
        "completion_models",
        ["completion_model_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    # Drop foreign key first
    op.drop_constraint(
        "fk_app_runs_completion_model_id", "app_runs", type_="foreignkey"
    )

    # Drop the column
    op.drop_column('app_runs', 'completion_model_id')
