"""cleanup
Revision ID: 455a34aa009c
Revises: 9751d5565531, dd1039b87a50
Create Date: 2024-05-27 07:52:56.490887
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = '455a34aa009c'
down_revision = ('9751d5565531', 'dd1039b87a50')
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint('crawls_groups_fkey', 'crawls', type_='foreignkey')
    op.drop_constraint(
        'agents_groups_groups_fkey', 'assistants_groups', type_='foreignkey'
    )
    op.drop_constraint(
        'usergroups_groups_groups_fkey', 'usergroups_groups', type_='foreignkey'
    )
    op.drop_constraint('info_blobs_groups_fkey', 'info_blobs', type_='foreignkey')
    op.drop_constraint(
        'services_groups_group_id_fkey', 'services_groups', type_='foreignkey'
    )

    # Cleanup
    op.drop_column('assistants', 'is_public')
    op.drop_index('ix_groups_uuid', 'groups')
    op.create_index(
        op.f('ix_info_blobs_group_id'), 'info_blobs', ['group_id'], unique=False
    )
    op.drop_index('ix_services_id', table_name='services')
    op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=False)
    op.drop_constraint('steps_assistant_id_fkey', 'steps', type_='foreignkey')
    op.create_foreign_key(
        'steps_services_fkey', 'steps', 'services', ['assistant_id'], ['id']
    )

    # Recreate the foreign keys
    op.create_foreign_key(
        'crawls_groups_fkey',
        'crawls',
        'groups',
        ['group_id'],
        ['id'],
        ondelete='SET NULL',
    )
    op.create_foreign_key(
        'assistants_groups_groups_fkey',
        'assistants_groups',
        'groups',
        ['group_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'usergroups_groups_groups_fkey',
        'usergroups_groups',
        'groups',
        ['group_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'info_blobs_groups_fkey',
        'info_blobs',
        'groups',
        ['group_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'services_groups_group_id_fkey',
        'services_groups',
        'groups',
        ['group_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint('steps_services_fkey', 'steps', type_='foreignkey')
    op.create_foreign_key(
        'steps_assistant_id_fkey',
        'steps',
        'services',
        ['assistant_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.create_index('ix_services_id', 'services', ['id'], unique=True)
    op.drop_index(op.f('ix_info_blobs_group_id'), table_name='info_blobs')
    op.add_column(
        'assistants',
        sa.Column(
            'is_public',
            sa.BOOLEAN(),
            autoincrement=False,
            nullable=False,
            server_default="false",
        ),
    )
