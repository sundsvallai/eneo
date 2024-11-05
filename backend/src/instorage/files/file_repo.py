# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from uuid import UUID

import sqlalchemy as sa

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.files_table import Files
from instorage.files.file_models import File, FileCreate


class FileRepository:
    def __init__(self, session: AsyncSession):
        self._delegate = BaseRepositoryDelegate(
            session=session, table=Files, in_db_model=File
        )
        self._session = session

    async def add(self, file: FileCreate) -> File:
        return await self._delegate.add(file)

    async def get_list_by_id_and_user(self, ids: list[UUID], user_id: UUID) -> File:
        stmt = (
            sa.select(Files)
            .where(Files.id.in_(ids))
            .where(Files.user_id == user_id)
            .order_by(Files.created_at)
        )

        files_in_db = await self._session.scalars(stmt)

        return [File.model_validate(file) for file in files_in_db]

    async def get_list_by_user(self, user_id: UUID) -> File:
        return await self._delegate.filter_by(conditions={Files.user_id: user_id})

    async def get_by_checksum(self, checksum: str) -> File:
        return await self._delegate.get_by(conditions={Files.checksum: checksum})

    async def delete(self, id: UUID) -> File:
        return await self._delegate.delete(id)
