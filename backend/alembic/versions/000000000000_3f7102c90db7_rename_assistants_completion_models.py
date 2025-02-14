"""rename assistants completion models
Revision ID: 3f7102c90db7
Revises: 3ce70f5c1e9f
Create Date: 2024-02-21 12:47:46.055638
"""

import sqlalchemy as sa

from alembic import op

UPGRADE_MAP = {
    "gpt-3.5-turbo-16k": "ChatGPT",
    "gpt-3.5-turbo": "ChatGPT",
    "gpt-4": "GPT-4",
    "gpt-4-turbo-preview": "GPT-4",
    "mistralai/Mixtral-8x7B-Instruct-v0.1": "Mixtral",
}
DOWNGRADE_MAP = dict((v, k) for k, v in UPGRADE_MAP.items())


# revision identifiers, used by Alembic
revision = '3f7102c90db7'
down_revision = '3ce70f5c1e9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    assistants = conn.execute(sa.text("SELECT * FROM assistants"))

    for assistant in assistants.fetchall():
        conn.execute(
            sa.text(
                "UPDATE assistants SET completion_model = :completion_model WHERE id = :id"
            ),
            parameters={
                "completion_model": UPGRADE_MAP[assistant.completion_model],
                "id": assistant.id,
            },
        )


def downgrade() -> None:
    conn = op.get_bind()

    assistants = conn.execute(sa.text("SELECT * FROM assistants"))

    for assistant in assistants.fetchall():
        conn.execute(
            sa.text(
                "UPDATE assistants SET completion_model = :completion_model WHERE id = :id"
            ),
            parameters={
                "completion_model": DOWNGRADE_MAP.get(
                    assistant.completion_model, "gpt-3.5-turbo"
                ),
                "id": assistant.id,
            },
        )
