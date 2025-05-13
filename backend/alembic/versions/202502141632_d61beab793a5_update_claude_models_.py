"""update_claude_models
Revision ID: d61beab793a5
Revises: a1d790d06842
Create Date: 2025-02-14 16:32:55.995624
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "d61beab793a5"
down_revision = "a1d790d06842"
branch_labels = None
depends_on = None


def upgrade() -> None:
    completion_models = sa.table("completion_models", sa.column("name", sa.String))

    # Update claude-3-opus-20240229 to claude-3-opus-latest
    op.execute(
        completion_models.update()
        .where(completion_models.c.name == "claude-3-opus-20240229")
        .values(name="claude-3-opus-latest")
    )

    # Update claude-3-5-sonnet-20240620 to claude-3-5-sonnet-latest
    op.execute(
        completion_models.update()
        .where(completion_models.c.name == "claude-3-5-sonnet-20240620")
        .values(name="claude-3-5-sonnet-latest")
    )


def downgrade() -> None:
    completion_models = sa.table("completion_models", sa.column("name", sa.String))

    # Revert claude-3-opus-latest to claude-3-opus-20240229
    op.execute(
        completion_models.update()
        .where(completion_models.c.name == "claude-3-opus-latest")
        .values(name="claude-3-opus-20240229")
    )

    # Revert claude-3-5-sonnet-latest to claude-3-5-sonnet-20240620
    op.execute(
        completion_models.update()
        .where(completion_models.c.name == "claude-3-5-sonnet-latest")
        .values(name="claude-3-5-sonnet-20240620")
    )
