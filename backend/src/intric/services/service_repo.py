from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from intric.database.database import AsyncSession
from intric.database.repositories.base import BaseRepositoryDelegate
from intric.database.tables.service_table import Services
from intric.services.service import Service, ServiceUpdate


class ServiceRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._delegate = BaseRepositoryDelegate(
            session, Services, Service, with_options=self._get_options()
        )

    @staticmethod
    def _get_options():
        return [
            selectinload(Services.user),
            selectinload(Services.groups),
            selectinload(Services.completion_model),
        ]

    async def add(self, service: ServiceUpdate) -> Service:
        return await self._delegate.add(service)

    async def get_by_id(self, id: UUID) -> Service:
        return await self._delegate.get(id)

    async def get_for_user(
        self, user_id: UUID, search_query: str = None
    ) -> list[Service]:
        stmt = (
            sa.select(Services)
            .where(Services.user_id == user_id)
            .order_by(Services.created_at)
        )

        if search_query is not None:
            stmt = stmt.filter(Services.name.like(f"%{search_query}%"))

        return await self._delegate.get_models_from_query(stmt)

    async def update(self, service: ServiceUpdate) -> Service:
        return await self._delegate.update(service)

    async def delete(self, id: UUID):
        query = sa.delete(Services).where(Services.id == id)
        await self._session.execute(query)

    async def add_service_to_space(self, service_id: UUID, space_id: UUID):
        stmt = (
            sa.update(Services)
            .where(Services.id == service_id)
            .values(space_id=space_id)
            .returning(Services)
        )

        return await self._delegate.get_model_from_query(stmt)
