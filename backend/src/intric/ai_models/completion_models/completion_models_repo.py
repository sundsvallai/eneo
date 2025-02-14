from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from intric.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelCreate,
    CompletionModelUpdate,
)
from intric.database.database import AsyncSession
from intric.database.repositories.base import BaseRepositoryDelegate
from intric.database.tables.ai_models_table import (
    CompletionModels,
    CompletionModelSettings,
)
from intric.main.exceptions import UniqueException
from intric.main.models import IdAndName


class CompletionModelsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.delegate = BaseRepositoryDelegate(
            session, CompletionModels, CompletionModel
        )

    async def _get_model_settings(self, id: UUID, tenant_id: UUID):
        query = sa.select(CompletionModelSettings).where(
            CompletionModelSettings.tenant_id == tenant_id,
            CompletionModelSettings.completion_model_id == id,
        )
        return await self.session.scalar(query)

    async def _get_models_settings_mapper(self, tenant_id: UUID):
        query = sa.select(CompletionModelSettings).where(
            CompletionModelSettings.tenant_id == tenant_id
        )
        settings = await self.session.scalars(query)
        return {s.completion_model_id: s.is_org_enabled for s in settings}

    async def get_model(self, id: UUID, tenant_id: UUID) -> CompletionModel:
        model = await self.delegate.get(id)

        settings = await self._get_model_settings(id, tenant_id)
        if settings:
            model.is_org_enabled = settings.is_org_enabled
        return model

    async def get_model_by_name(self, name: str) -> CompletionModel:
        return await self.delegate.get_by(conditions={CompletionModels.name: name})

    async def create_model(self, model: CompletionModelCreate) -> CompletionModel:
        return await self.delegate.add(model)

    async def enable_completion_model(
        self,
        is_org_enabled: bool,
        completion_model_id: UUID,
        tenant_id: UUID,
    ):
        query = sa.select(CompletionModelSettings).where(
            CompletionModelSettings.tenant_id == tenant_id,
            CompletionModelSettings.completion_model_id == completion_model_id,
        )
        settings = await self.session.scalar(query)

        try:
            if settings:
                query = (
                    sa.update(CompletionModelSettings)
                    .values(is_org_enabled=is_org_enabled)
                    .where(
                        CompletionModelSettings.tenant_id == tenant_id,
                        CompletionModelSettings.completion_model_id
                        == completion_model_id,
                    )
                    .returning(CompletionModelSettings)
                )
                return await self.session.scalar(query)
            query = (
                sa.insert(CompletionModelSettings)
                .values(
                    is_org_enabled=is_org_enabled,
                    completion_model_id=completion_model_id,
                    tenant_id=tenant_id,
                )
                .returning(CompletionModelSettings)
            )
            return await self.session.scalar(query)
        except IntegrityError as e:
            raise UniqueException("Default completion model already exists.") from e

    async def update_model(self, model: CompletionModelUpdate) -> CompletionModel:
        return await self.delegate.update(model)

    async def delete_model(self, id: UUID) -> CompletionModel:
        stmt = (
            sa.delete(CompletionModels)
            .where(CompletionModels.id == id)
            .returning(CompletionModels)
        )

        await self.delegate.get_record_from_query(stmt)

    async def get_models(
        self,
        tenant_id: UUID = None,
        is_deprecated: bool = False,
        id_list: list[UUID] = None,
    ) -> list[CompletionModel]:
        query = (
            sa.select(CompletionModels)
            .where(CompletionModels.is_deprecated == is_deprecated)
            .order_by(CompletionModels.created_at)
        )

        if id_list is not None:
            query = query.where(CompletionModels.id.in_(id_list))

        models = await self.delegate.get_models_from_query(query)

        if tenant_id is not None:
            settings_mapper = await self._get_models_settings_mapper(tenant_id)

            for model in models:
                model.is_org_enabled = settings_mapper.get(model.id, False)

        return models

    async def get_ids_and_names(self) -> list[(UUID, str)]:
        stmt = sa.select(CompletionModels)

        models = await self.delegate.get_records_from_query(stmt)

        return [IdAndName(id=model.id, name=model.name) for model in models.all()]
