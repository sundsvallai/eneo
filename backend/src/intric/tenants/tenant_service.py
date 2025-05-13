from typing import TYPE_CHECKING
from uuid import UUID

from intric.main.exceptions import NotFoundException
from intric.main.models import ModelId
from intric.tenants.tenant import (
    TenantBase,
    TenantInDB,
    TenantUpdate,
    TenantUpdatePublic,
)
from intric.tenants.tenant_repo import TenantRepository

if TYPE_CHECKING:
    from intric.ai_models.completion_models.completion_models_repo import (
        CompletionModelsRepository,
    )
    from intric.ai_models.embedding_models.embedding_models_repo import (
        AdminEmbeddingModelsService,
    )
    from intric.transcription_models.infrastructure import (
        TranscriptionModelEnableService,
    )


class TenantService:
    def __init__(
        self,
        repo: TenantRepository,
        completion_model_repo: "CompletionModelsRepository",
        embedding_model_repo: "AdminEmbeddingModelsService",
        transcription_model_enable_service: "TranscriptionModelEnableService",
    ):
        self.repo = repo
        self.completion_model_repo = completion_model_repo
        self.embedding_model_repo = embedding_model_repo
        self.transcription_models_enable_service = transcription_model_enable_service

    @staticmethod
    def _validate(tenant: TenantInDB | None, id: UUID):
        if not tenant:
            raise NotFoundException(f"Tenant {id} not found")

    async def get_all_tenants(self, domain: str | None) -> list[TenantInDB]:
        return await self.repo.get_all_tenants(domain=domain)

    async def get_tenant_by_id(self, id: UUID) -> TenantInDB:
        tenant = await self.repo.get(id)
        self._validate(tenant, id)

        return tenant

    async def create_tenant(self, tenant: TenantBase) -> TenantInDB:
        tenant_in_db = await self.repo.add(tenant)

        default_completion_model = "gpt-4o"
        gpt_4o = await self.completion_model_repo.get_model_by_name(name=default_completion_model)

        await self.completion_model_repo.enable_completion_model(
            is_org_enabled=True,
            completion_model_id=gpt_4o.id,
            tenant_id=tenant_in_db.id,
        )

        default_embedding_model = "text-embedding-3-small"
        text_embedding_3_small = await self.embedding_model_repo.get_model_by_name(
            default_embedding_model
        )

        await self.embedding_model_repo.enable_embedding_model(
            is_org_enabled=True,
            embedding_model_id=text_embedding_3_small.id,
            tenant_id=tenant_in_db.id,
        )

        default_transcription_model = "whisper-1"
        whisper_1_id = await self.transcription_models_enable_service.get_model_id_by_name(
            model_name=default_transcription_model
        )
        await self.transcription_models_enable_service.enable_transcription_model(
            transcription_model_id=whisper_1_id,
            tenant_id=tenant_in_db.id,
            is_org_enabled=True,
            is_org_default=True,
        )

        return tenant_in_db

    async def delete_tenant(self, tenant_id: UUID) -> TenantInDB:
        tenant = await self.get_tenant_by_id(tenant_id)
        self._validate(tenant, tenant_id)

        return await self.repo.delete_tenant_by_id(tenant_id)

    async def update_tenant(self, tenant_update: TenantUpdatePublic, id: UUID) -> TenantInDB:
        tenant = await self.get_tenant_by_id(id)
        self._validate(tenant, id)

        tenant_update = TenantUpdate(**tenant_update.model_dump(exclude_unset=True), id=tenant.id)
        return await self.repo.update_tenant(tenant_update)

    async def add_modules(self, list_of_module_ids: list[ModelId], tenant_id: UUID):
        return await self.repo.add_modules(list_of_module_ids, tenant_id)
