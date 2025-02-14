"""Add model column to questions
Revision ID: 9365c76afc7c
Revises: d8f7c2465854
Create Date: 2023-06-16 22:06:25.810825
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "9365c76afc7c"
down_revision = "d8f7c2465854"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "questions",
        sa.Column(
            "model",
            sa.Text,
            nullable=True,
        ),
    )

    op.execute("UPDATE questions SET model = 'gpt-3.5-turbo'")
    op.alter_column("questions", "model", nullable=False)


def downgrade() -> None:
    op.drop_column("questions", "model")
