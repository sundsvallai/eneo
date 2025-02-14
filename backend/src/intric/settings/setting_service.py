from intric.ai_models.ai_models_service import AIModelsService
from intric.main.logging import get_logger
from intric.settings.settings import SettingsPublic, SettingsUpsert
from intric.settings.settings_repo import SettingsRepository
from intric.users.user import UserInDB

logger = get_logger(__name__)


class SettingService:
    def __init__(
        self,
        repo: SettingsRepository,
        user: UserInDB,
        ai_models_service: AIModelsService,
    ):
        self.repo = repo
        self.user = user
        self.ai_models_service = ai_models_service

    async def get_settings(self):
        settings = await self.repo.get(self.user.id)

        return settings

    async def update_settings(self, settings: SettingsPublic):
        settings_upsert = SettingsUpsert(**settings.model_dump(), user_id=self.user.id)

        settings_in_db = await self.repo.update(settings_upsert)
        logger.info(
            "Updated settings: %s for user: %s" % (settings_upsert, self.user.username)
        )

        return settings_in_db

    async def get_available_completion_models(self):
        return await self.ai_models_service.get_completion_models()

    async def get_available_embedding_models(self):
        return await self.ai_models_service.get_embedding_models()
