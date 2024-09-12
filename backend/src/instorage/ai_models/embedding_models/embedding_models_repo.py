from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelCreate,
    EmbeddingModelUpdate,
)
from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.ai_models_table import (
    EmbeddingModels,
    EmbeddingModelSettings,
)
from instorage.main.exceptions import UniqueException
from instorage.main.models import IdAndName


class EmbeddingModelsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.delegate = BaseRepositoryDelegate(session, EmbeddingModels, EmbeddingModel)

    async def _get_model_settings(self, id: UUID, tenant_id: UUID):
        query = sa.select(EmbeddingModelSettings).where(
            EmbeddingModelSettings.tenant_id == tenant_id,
            EmbeddingModelSettings.embedding_model_id == id,
        )
        return await self.session.scalar(query)

    async def _get_models_settings_mapper(self, tenant_id: UUID):
        query = sa.select(EmbeddingModelSettings).where(
            EmbeddingModelSettings.tenant_id == tenant_id
        )
        settings = await self.session.scalars(query)
        return {s.embedding_model_id: s.is_org_enabled for s in settings}

    async def get_model(self, id: UUID, tenant_id: UUID) -> EmbeddingModel:
        model = await self.delegate.get(id)

        settings = await self._get_model_settings(id, tenant_id)
        if settings:
            model.is_org_enabled = settings.is_org_enabled
        return model

    async def get_model_by_name(self, name: str) -> EmbeddingModel:
        return await self.delegate.get_by(conditions={EmbeddingModels.name: name})

    async def create_model(self, model: EmbeddingModelCreate) -> EmbeddingModel:
        return await self.delegate.add(model)

    async def update_model(self, model: EmbeddingModelUpdate) -> EmbeddingModel:
        return await self.delegate.update(model)

    async def delete_model(self, id: UUID) -> EmbeddingModel:
        return await self.delegate.delete(id)

    async def get_models(
        self,
        tenant_id: UUID = None,
        is_deprecated: bool = False,
        id_list: list[UUID] = None,
    ):
        stmt = (
            sa.select(EmbeddingModels)
            .where(EmbeddingModels.is_deprecated == is_deprecated)
            .order_by(EmbeddingModels.created_at)
        )

        if id_list is not None:
            stmt = stmt.where(EmbeddingModels.id.in_(id_list))

        models = await self.delegate.get_models_from_query(stmt)

        settings_mapper = await self._get_models_settings_mapper(tenant_id)

        for model in models:
            model.is_org_enabled = settings_mapper.get(model.id, False)

        return models

    async def get_ids_and_names(self) -> list[(UUID, str)]:
        stmt = sa.select(EmbeddingModels)

        models = await self.delegate.get_records_from_query(stmt)

        return [IdAndName(id=model.id, name=model.name) for model in models.all()]

    async def enable_embedding_model(
        self,
        is_org_enabled: bool,
        embedding_model_id: UUID,
        tenant_id: UUID,
    ):
        query = sa.select(EmbeddingModelSettings).where(
            EmbeddingModelSettings.tenant_id == tenant_id,
            EmbeddingModelSettings.embedding_model_id == embedding_model_id,
        )
        settings = await self.session.scalar(query)

        try:
            if settings:
                query = (
                    sa.update(EmbeddingModelSettings)
                    .values(is_org_enabled=is_org_enabled)
                    .where(
                        EmbeddingModelSettings.tenant_id == tenant_id,
                        EmbeddingModelSettings.embedding_model_id == embedding_model_id,
                    )
                    .returning(EmbeddingModelSettings)
                )
                return await self.session.scalar(query)
            query = (
                sa.insert(EmbeddingModelSettings)
                .values(
                    is_org_enabled=is_org_enabled,
                    embedding_model_id=embedding_model_id,
                    tenant_id=tenant_id,
                )
                .returning(EmbeddingModelSettings)
            )
            return await self.session.scalar(query)
        except IntegrityError as e:
            raise UniqueException("Default embedding model already exists.") from e
