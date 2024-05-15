from fastapi import Depends

from instorage.authentication.auth_dependencies import (
    get_user_from_token_or_assistant_api_key_without_assistant_id,
)
from instorage.main.container import Container
from instorage.server.dependencies.container import get_container
from instorage.server.dependencies.db import get_repository
from instorage.settings.setting_service import SettingService
from instorage.settings.settings_repo import SettingsRepository
from instorage.users.user import UserInDB


def get_settings_service(
    container: Container = Depends(get_container(with_user=True)),
):
    return container.settings_service()


def get_settings_service_allowing_read_only_key(
    user: UserInDB = Depends(
        get_user_from_token_or_assistant_api_key_without_assistant_id
    ),
    repo: SettingsRepository = Depends(get_repository(SettingsRepository)),
):
    return SettingService(repo, user)
