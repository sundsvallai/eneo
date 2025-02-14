"""prompts many-to-many
Revision ID: b521d9dc42ed
Revises: 8e535b29ecfa
Create Date: 2024-10-14 10:10:31.163873
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = 'b521d9dc42ed'
down_revision = '8e535b29ecfa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the new many-to-many table
    op.create_table(
        'prompts_assistants',
        sa.Column('prompt_id', sa.UUID(), nullable=False),
        sa.Column('assistant_id', sa.UUID(), nullable=False),
        sa.Column('is_selected', sa.Boolean, nullable=False),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['assistant_id'], ['assistants.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(['prompt_id'], ['prompts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('prompt_id', 'assistant_id'),
    )

    # Data migration
    connection = op.get_bind()

    # Set all prompts is_selected to False
    connection.execute(
        sa.text(
            """
            UPDATE prompts SET is_selected = False
            """
        )
    )

    # Migrate data from assistants table to prompts
    connection.execute(
        sa.text(
            """
            INSERT INTO prompts (text, is_selected, user_id, tenant_id, assistant_id)
            SELECT a.prompt, True, a.user_id, u.tenant_id, a.id
            FROM assistants a
            JOIN users u
            ON u.id = a.user_id
            """
        )
    )

    # Migrate data from prompts table to prompts_assistants
    connection.execute(
        sa.text(
            """
            INSERT INTO prompts_assistants (prompt_id, assistant_id, is_selected)
            SELECT id, assistant_id, is_selected FROM prompts
            """
        )
    )

    # Drop old columns
    op.drop_constraint('prompts_assistant_id_fkey', 'prompts', type_='foreignkey')
    op.drop_column('prompts', 'assistant_id')
    op.drop_column('prompts', 'is_selected')
    op.drop_column('assistants', 'prompt')


def downgrade() -> None:
    # Add back old columns
    op.add_column(
        'prompts',
        sa.Column('assistant_id', sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column('prompts', sa.Column('is_selected', sa.Boolean, nullable=True))
    op.create_foreign_key(
        'prompts_assistant_id_fkey',
        'prompts',
        'assistants',
        ['assistant_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.add_column(
        'assistants',
        sa.Column('prompt', sa.VARCHAR(), autoincrement=False, nullable=True),
    )

    # Data migration for downgrade
    connection = op.get_bind()

    # Migrate data back to prompts table
    connection.execute(
        sa.text(
            """
            UPDATE prompts p
            SET assistant_id = pa.assistant_id, is_selected = pa.is_selected
            FROM prompts_assistants pa
            WHERE p.id = pa.prompt_id
            """
        )
    )

    # Migrate data back to assistants table
    connection.execute(
        sa.text(
            """
            UPDATE assistants a
            SET prompt = p.text
            FROM prompts p
            JOIN prompts_assistants pa ON p.id = pa.prompt_id
            WHERE a.id = pa.assistant_id
            AND is_selected
            """
        )
    )

    # Drop the many-to-many table
    op.drop_table('prompts_assistants')

    # Make columns non-nullable if needed
    op.alter_column('prompts', 'assistant_id', nullable=False)
    op.alter_column('prompts', 'is_selected', nullable=False)
    op.alter_column('assistants', 'prompt', nullable=False)
