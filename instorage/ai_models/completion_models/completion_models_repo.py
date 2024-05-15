from typing import List
from uuid import UUID

from instorage.ai_models.completion_models.completion_model import (
    CompletionModelCreate,
    CompletionModelInDB,
    CompletionModelUpdate,
)
from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.ai_models_table import CompletionModels


class CompletionModelsRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session, CompletionModels, CompletionModelInDB
        )

    async def get_model(self, id: UUID) -> CompletionModelInDB:
        return await self.delegate.get(id)

    async def create_model(self, model: CompletionModelCreate) -> CompletionModelInDB:
        return await self.delegate.add(model)

    async def update_model(self, model: CompletionModelUpdate) -> CompletionModelInDB:
        return await self.delegate.update(model)

    async def delete_model(self, id: UUID) -> CompletionModelInDB:
        return await self.delegate.delete(id)

    async def get_models(self, selectable: bool = None) -> List[CompletionModelInDB]:
        conditions = {}
        if selectable is not None:
            conditions = {CompletionModels.selectable: selectable}

        return await self.delegate.filter_by(conditions=conditions)
