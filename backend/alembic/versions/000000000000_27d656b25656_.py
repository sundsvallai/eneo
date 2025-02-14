"""empty message
Revision ID: 27d656b25656
Revises: 73f42a3b4915
Create Date: 2024-11-22 11:00:15.617483
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic
revision = "27d656b25656"
down_revision = "73f42a3b4915"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "assistant_templates",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.VARCHAR(100), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("category", sa.VARCHAR(10), nullable=False),
        sa.Column("prompt_text", sa.Text, nullable=False),
        sa.Column("completion_model_kwargs", JSONB, nullable=True),
        sa.Column("wizard", JSONB, nullable=True),
        sa.Column(
            "completion_model_id",
            UUID(as_uuid=True),
            sa.ForeignKey("completion_models.id"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("assistant_templates")
