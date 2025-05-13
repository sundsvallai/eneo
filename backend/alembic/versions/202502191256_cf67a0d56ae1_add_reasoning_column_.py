"""add_reasoning_column
Revision ID: cf67a0d56ae1
Revises: d61beab793a5
Create Date: 2025-02-19 12:56:26.736784
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "cf67a0d56ae1"
down_revision = "d61beab793a5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add the column allowing NULL temporarily
    op.add_column(
        "completion_models", sa.Column("reasoning", sa.Boolean(), nullable=True)
    )

    # update all rows to false by default
    op.execute("UPDATE completion_models SET reasoning = false")

    # update 'o3-mini'
    op.execute("UPDATE completion_models SET reasoning = true WHERE name = 'o3-mini'")

    # make the column non-nullable
    op.alter_column(
        "completion_models", "reasoning", existing_type=sa.Boolean(), nullable=False
    )


def downgrade() -> None:
    op.drop_column("completion_models", "reasoning")
