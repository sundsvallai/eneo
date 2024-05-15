from instorage.ai_models.completion_models.llms import (
    CompletionModel,
    ModelHostingLocation,
    supported_models,
)
from instorage.ai_models.embedding_models.embedding_models import EmbeddingModel
from instorage.ai_models.embedding_models.embedding_models import (
    supported_models as supported_embedding_models,
)
from instorage.main.logging import get_logger
from instorage.modules.module import Modules
from instorage.settings.settings import SettingsPublic, SettingsUpsert
from instorage.settings.settings_repo import SettingsRepository
from instorage.users.user import UserInDB

logger = get_logger(__name__)


class SettingService:
    def __init__(
        self,
        repo: SettingsRepository,
        user: UserInDB,
    ):
        self.repo = repo
        self.user = user

    def _set_access_rights(self, models: list[CompletionModel | EmbeddingModel]):
        for model in models:
            if (
                model.hosting == ModelHostingLocation.EU
                and Modules.EU_HOSTING not in self.user.modules
            ):
                model.can_access = False

        return models

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

    def get_available_completion_models(self):
        return self._set_access_rights(supported_models())

    def get_available_embedding_models(self):
        return self._set_access_rights(supported_embedding_models())
