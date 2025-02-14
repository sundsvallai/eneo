"""add token count column
Revision ID: 63f7e27b67cc
Revises: 9365c76afc7c
Create Date: 2023-06-27 13:00:29.091708
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "63f7e27b67cc"
down_revision = "9365c76afc7c"
branch_labels = None
depends_on = None

TOKEN_COLUMN_NAME = "used_tokens"
USERS_COLUMN_NAME = "users"


def upgrade() -> None:
    op.add_column(
        USERS_COLUMN_NAME, sa.Column(TOKEN_COLUMN_NAME, sa.Integer, nullable=True)
    )
    op.execute(f"UPDATE {USERS_COLUMN_NAME} SET {TOKEN_COLUMN_NAME} = 0")
    op.alter_column(USERS_COLUMN_NAME, TOKEN_COLUMN_NAME, nullable=False)


def downgrade() -> None:
    op.drop_column(USERS_COLUMN_NAME, TOKEN_COLUMN_NAME)
