"""Fix existing db columns
Revision ID: c353278d225f
Revises: f152079c27aa
Create Date: 2024-12-03 15:18:51.457072
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "c353278d225f"
down_revision = "f152079c27aa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "assistant_templates",
        "prompt_text",
        existing_nullable=False,
        nullable=True,
    )
    op.alter_column(
        "assistant_templates",
        "category",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "assistant_templates",
        "prompt_text",
        existing_nullable=True,
        nullable=False,
    )
    op.alter_column(
        "assistant_templates",
        "category",
        existing_type=sa.VARCHAR(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
    )
