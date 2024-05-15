from uuid import UUID

import sqlalchemy as sa

from instorage.allowed_origins.allowed_origin_models import AllowedOriginInDB
from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.allowed_origins_table import AllowedOrigins


class AllowedOriginRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session=session, table=AllowedOrigins, in_db_model=AllowedOriginInDB
        )

    async def add(self, origins: list[str], tenant_id: int):
        stmt = (
            sa.insert(AllowedOrigins)
            .values([dict(url=origin, tenant_id=tenant_id) for origin in origins])
            .returning(AllowedOrigins)
        )

        return await self.delegate.get_models_from_query(stmt)

    async def get_origin(self, origin: str):
        stmt = sa.select(AllowedOrigins).where(AllowedOrigins.url == origin)

        return await self.delegate.get_model_from_query(stmt)

    async def get_all(self, tenant_id: int):
        return await self.delegate.filter_by(
            conditions={AllowedOrigins.tenant_id: tenant_id}
        )

    async def delete(self, id: UUID):
        return await self.delegate.delete_by_uuid(id)
