from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import defer, selectinload

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.users_table import Users
from instorage.info_blobs.info_blob import (
    InfoBlobAdd,
    InfoBlobAddToDB,
    InfoBlobInDB,
    InfoBlobInDBNoText,
    InfoBlobUpdate,
)


class InfoBlobRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            InfoBlobs,
            InfoBlobInDB,
            with_options=[selectinload(InfoBlobs.group)],
        )
        self.session = session

    async def _get_group(self, group_id: UUID):
        stmt = sa.select(Groups).where(Groups.uuid == group_id)
        group = await self.session.scalar(stmt)

        return group

    async def add(self, info_blob: InfoBlobAdd):
        group = await self._get_group(info_blob.group_id)
        info_blob_to_db = InfoBlobAddToDB(
            **info_blob.model_dump(exclude={"group_id"}),
            id=uuid4().hex,
            group_id=group.id,
            embedding_model=group.embedding_model
        )

        return await self.delegate.add(info_blob_to_db)

    async def update(self, info_blob: InfoBlobUpdate) -> InfoBlobInDB:
        return await self.delegate.update(info_blob)

    async def get_by_user(self, user_id: int):
        query = (
            sa.select(InfoBlobs)
            .where(InfoBlobs.user_id == user_id)
            .order_by(InfoBlobs.created_at)
            .options(selectinload(InfoBlobs.group))
            .options(defer(InfoBlobs.text))
        )
        items = await self.delegate.get_records_from_query(query)
        return [InfoBlobInDBNoText.model_validate(record) for record in items]

    async def get(self, id: int):
        return await self.delegate.get(id)

    async def get_by_group(self, group_id: int) -> list[InfoBlobInDB]:
        query = (
            sa.select(InfoBlobs)
            .where(InfoBlobs.group_id == group_id)
            .order_by(InfoBlobs.created_at)
            .options(selectinload(InfoBlobs.group))
        )
        return await self.delegate.get_models_from_query(query)

    async def delete(self, id: int) -> InfoBlobInDB:
        return await self.delegate.delete(id)

    async def get_count_of_group(self, group_id: int):
        stmt = (
            sa.select(sa.func.count())
            .select_from(InfoBlobs)
            .where(InfoBlobs.group_id == group_id)
        )

        return await self.session.scalar(stmt)

    def _sum_stmt(self):
        return sa.select(sa.func.sum(InfoBlobs.size)).select_from(InfoBlobs)

    async def get_total_size_of_group(self, group_id: int):
        stmt = self._sum_stmt().where(InfoBlobs.group_id == group_id)

        size = await self.session.scalar(stmt)

        if size is None:
            return 0

        return size

    async def get_total_size_of_user(self, user_id: int):
        stmt = self._sum_stmt().where(InfoBlobs.user_id == user_id)

        size = await self.session.scalar(stmt)

        if size is None:
            return 0

        return size

    async def get_total_size_of_tenant(self, tenant_id: int):
        stmt = self._sum_stmt().join(Users).where(Users.tenant_id == tenant_id)

        size = await self.session.scalar(stmt)

        if size is None:
            return 0

        return size

    async def get_ids(self):
        stmt = sa.select(InfoBlobs.id)

        ids = await self.session.scalars(stmt)

        return set(ids)

    async def get_by_uuid(self, uuid: UUID):
        return await self.delegate.get_by(conditions={InfoBlobs.uuid: uuid})
