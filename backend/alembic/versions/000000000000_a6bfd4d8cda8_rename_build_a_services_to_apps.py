"""rename build-a-services to apps
Revision ID: a6bfd4d8cda8
Revises: 32ab8c79cd83
Create Date: 2024-10-17 10:06:55.539242
"""

from alembic import op

# revision identifiers, used by Alembic
revision = 'a6bfd4d8cda8'
down_revision = '32ab8c79cd83'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename tables
    op.rename_table('build_a_services', 'apps')
    op.rename_table('build_a_service_files', 'apps_files')
    op.rename_table('build_a_services_prompts', 'apps_prompts')

    # Rename columns in the app_files table
    op.alter_column('apps_files', 'build_a_service_id', new_column_name='app_id')

    # Rename columns in the app_prompts table
    op.alter_column('apps_prompts', 'build_a_service_id', new_column_name='app_id')

    # Rename columns in the app_input_fields table
    op.alter_column('input_fields', 'build_a_service_id', new_column_name='app_id')


def downgrade() -> None:
    # Rename columns back in the app_input_fields table
    op.alter_column('input_fields', 'app_id', new_column_name='build_a_service_id')

    # Rename columns back in the app_prompts table
    op.alter_column('apps_prompts', 'app_id', new_column_name='build_a_service_id')

    # Rename columns back in the app_files table
    op.alter_column('apps_files', 'app_id', new_column_name='build_a_service_id')

    # Rename tables back
    op.rename_table('apps_prompts', 'build_a_services_prompts')
    op.rename_table('apps_files', 'build_a_service_files')
    op.rename_table('apps', 'build_a_services')
