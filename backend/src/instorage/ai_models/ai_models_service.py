from uuid import UUID

from instorage.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelFamily,
    CompletionModelPublic,
    CompletionModelUpdateFlags,
    ModelHostingLocation,
)
from instorage.ai_models.completion_models.completion_models_repo import (
    CompletionModelsRepository,
)
from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelPublic,
    EmbeddingModelUpdateFlags,
)
from instorage.ai_models.embedding_models.embedding_models_repo import (
    EmbeddingModelsRepository,
)
from instorage.main.config import get_settings
from instorage.main.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from instorage.modules.module import Modules
from instorage.roles.permissions import Permission, validate_permissions
from instorage.tenants.tenant_repo import TenantRepository
from instorage.users.user import UserInDB


class AIModelsService:
    def __init__(
        self,
        user: UserInDB,
        embedding_model_repo: EmbeddingModelsRepository,
        completion_model_repo: CompletionModelsRepository,
        tenant_repo: TenantRepository,
    ):
        self.user = user
        self.embedding_model_repo = embedding_model_repo
        self.completion_model_repo = completion_model_repo
        self.tenant_repo = tenant_repo

    def _is_locked(
        self,
        model: CompletionModel | EmbeddingModel,
    ):
        if model.hosting == ModelHostingLocation.EU:
            if Modules.EU_HOSTING not in self.user.modules:
                return True
        return False

    def _can_access(
        self,
        model: CompletionModel | EmbeddingModel,
    ):
        if (
            not self._is_locked(model)
            and not model.is_deprecated
            and model.is_org_enabled
        ):
            return True

        return False

    def _get_latest_available_model(
        self, models: list[CompletionModelPublic | EmbeddingModelPublic]
    ):
        sorted_models = sorted(models, key=lambda model: model.created_at, reverse=True)

        for model in sorted_models:
            if model.can_access:
                return model

    async def get_embedding_models(
        self, id_list: list[UUID] = None
    ) -> list[EmbeddingModelPublic]:
        embedding_models = await self.embedding_model_repo.get_models(
            tenant_id=self.user.tenant_id, is_deprecated=False, id_list=id_list
        )

        models = []
        for model in embedding_models:
            models.append(
                EmbeddingModelPublic(
                    **model.model_dump(),
                    is_locked=self._is_locked(model),
                    can_access=self._can_access(model),
                )
            )

        return models

    async def get_embedding_model(self, id: UUID):
        model = await self.embedding_model_repo.get_model(
            id, tenant_id=self.user.tenant_id
        )

        if model.is_deprecated:
            raise BadRequestException(
                f"EmbeddingModel {model.name} not supported anymore."
            )

        can_access = self._can_access(model)
        if not can_access:
            raise UnauthorizedException(
                "Unauthorized. User has no permissions to access."
            )

        return EmbeddingModelPublic(
            **model.model_dump(),
            is_locked=self._is_locked(model),
            can_access=can_access,
        )

    async def get_latest_available_embedding_model(self):
        models = await self.get_embedding_models()

        return self._get_latest_available_model(models)

    async def get_completion_models(
        self, id_list: list[UUID] = None
    ) -> list[CompletionModelPublic]:
        completion_models = await self.completion_model_repo.get_models(
            tenant_id=self.user.tenant_id,
            is_deprecated=False,
            id_list=id_list,
        )

        models = []
        for model in completion_models:
            if (
                model.family == CompletionModelFamily.AZURE
                and not get_settings().using_azure_models
            ):
                continue

            models.append(
                CompletionModelPublic(
                    **model.model_dump(),
                    is_locked=self._is_locked(model),
                    can_access=self._can_access(model),
                )
            )

        return models

    async def get_completion_model(self, id: UUID):
        model = await self.completion_model_repo.get_model(
            id, tenant_id=self.user.tenant_id
        )

        if (
            model.family == CompletionModelFamily.AZURE
            and not get_settings().using_azure_models
        ):
            raise NotFoundException()

        if model.is_deprecated:
            raise BadRequestException(
                f"CompletionModel {model.name} not supported anymore."
            )

        can_access = self._can_access(model)
        if not can_access:
            raise UnauthorizedException(
                "Unauthorized. User has no permissions to access."
            )

        return CompletionModelPublic(
            **model.model_dump(),
            is_locked=self._is_locked(model),
            can_access=can_access,
        )

    async def get_latest_available_completion_model(self):
        models = await self.get_completion_models()

        return self._get_latest_available_model(models)

    @validate_permissions(Permission.ADMIN)
    async def enable_completion_model(
        self, completion_model_id: UUID, data: CompletionModelUpdateFlags
    ):
        await self.completion_model_repo.enable_completion_model(
            is_org_enabled=data.is_org_enabled,
            completion_model_id=completion_model_id,
            tenant_id=self.user.tenant_id,
        )

        model = await self.completion_model_repo.get_model(
            completion_model_id, tenant_id=self.user.tenant_id
        )
        return CompletionModelPublic(
            **model.model_dump(),
            is_locked=self._is_locked(model),
            can_access=self._can_access(model),
        )

    @validate_permissions(Permission.ADMIN)
    async def enable_embedding_model(
        self, embedding_model_id: UUID, data: EmbeddingModelUpdateFlags
    ):
        await self.embedding_model_repo.enable_embedding_model(
            is_org_enabled=data.is_org_enabled,
            embedding_model_id=embedding_model_id,
            tenant_id=self.user.tenant_id,
        )

        model = await self.embedding_model_repo.get_model(
            embedding_model_id, tenant_id=self.user.tenant_id
        )
        return EmbeddingModelPublic(
            **model.model_dump(),
            is_locked=self._is_locked(model),
            can_access=self._can_access(model),
        )
