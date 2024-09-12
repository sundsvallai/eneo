# MIT license

from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from instorage.ai_models.completion_models.completion_model import CompletionModelSparse
from instorage.ai_models.embedding_models.embedding_model import EmbeddingModelSparse
from instorage.database.database import AsyncSession
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.spaces_table import (
    Spaces,
    SpacesCompletionModels,
    SpacesEmbeddingModels,
    SpacesUsers,
)
from instorage.database.tables.websites_table import CrawlRuns, Websites
from instorage.main.exceptions import UniqueException
from instorage.spaces.api.space_models import SpaceMember
from instorage.spaces.space import Space
from instorage.spaces.space_factory import SpaceFactory


class SpaceRepository:
    def __init__(self, session: AsyncSession, factory: SpaceFactory):
        self.session = session
        self.factory = factory

    def _options(self):
        return [
            selectinload(Spaces.embedding_models),
            selectinload(Spaces.completion_models),
            selectinload(Spaces.members).selectinload(SpacesUsers.user),
            selectinload(Spaces.assistants),
            selectinload(Spaces.services),
            selectinload(Spaces.websites)
            .selectinload(Websites.latest_crawl)
            .selectinload(CrawlRuns.job),
            selectinload(Spaces.websites).selectinload(Websites.embedding_model),
        ]

    async def _get_groups(self, space_id: UUID):
        query = (
            sa.select(
                Groups,
                sa.func.coalesce(sa.func.count(InfoBlobs.id).label("infoblob_count")),
            )
            .outerjoin(InfoBlobs, Groups.id == InfoBlobs.group_id)
            .where(Groups.space_id == space_id)
            .group_by(Groups.id)
            .order_by(Groups.created_at)
            .options(selectinload(Groups.embedding_model))
        )

        res = await self.session.execute(query)
        return res.all()

    async def _set_embedding_models(
        self, space_in_db: Spaces, embedding_models: list[EmbeddingModelSparse]
    ):
        # Delete all
        stmt = sa.delete(SpacesEmbeddingModels).where(
            SpacesEmbeddingModels.space_id == space_in_db.id
        )
        await self.session.execute(stmt)

        if embedding_models:
            stmt = sa.insert(SpacesEmbeddingModels).values(
                [
                    dict(embedding_model_id=embedding_model.id, space_id=space_in_db.id)
                    for embedding_model in embedding_models
                ]
            )
            await self.session.execute(stmt)

        # This allows the embedding models to be reflected in the space object
        await self.session.refresh(space_in_db)

    async def _set_completion_models(
        self, space_in_db: Spaces, completion_models: list[CompletionModelSparse]
    ):
        # Delete all
        stmt = sa.delete(SpacesCompletionModels).where(
            SpacesCompletionModels.space_id == space_in_db.id
        )
        await self.session.execute(stmt)

        if completion_models:
            stmt = sa.insert(SpacesCompletionModels).values(
                [
                    dict(
                        completion_model_id=completion_model.id, space_id=space_in_db.id
                    )
                    for completion_model in completion_models
                ]
            )
            await self.session.execute(stmt)

        # This allows the completion models to be reflected in the space object
        await self.session.refresh(space_in_db)

    async def _set_members(self, space_in_db: Spaces, members: dict[UUID, SpaceMember]):
        # Delete all
        stmt = sa.delete(SpacesUsers).where(SpacesUsers.space_id == space_in_db.id)
        await self.session.execute(stmt)

        # Add members
        if members:
            spaces_users = [
                dict(
                    space_id=space_in_db.id,
                    user_id=member.id,
                    role=member.role.value,
                )
                for member in members.values()
            ]

            stmt = sa.insert(SpacesUsers).values(spaces_users)
            await self.session.execute(stmt)

        # This allows the newly added members to be reflected in the space
        await self.session.refresh(space_in_db)

    async def _get_from_query(self, query: sa.Select):
        entry_in_db = await self.get_record_with_options(query)

        if not entry_in_db:
            return

        groups = await self._get_groups(entry_in_db.id)

        return self.factory.create_space_from_db(entry_in_db, groups_in_db=groups)

    async def get_record_with_options(self, query):
        for option in self._options():
            query = query.options(option)

        return await self.session.scalar(query)

    async def get_records_with_options(self, query):
        for option in self._options():
            query = query.options(option)

        return await self.session.scalars(query)

    async def add(self, space: Space) -> Space:
        query = (
            sa.insert(Spaces)
            .values(
                name=space.name,
                description=space.description,
                tenant_id=space.tenant_id,
                user_id=space.user_id,
            )
            .returning(Spaces)
        )

        try:
            entry_in_db = await self.get_record_with_options(query)
        except IntegrityError as e:
            raise UniqueException("Users can only have one personal space") from e

        await self._set_completion_models(entry_in_db, space.completion_models)
        await self._set_embedding_models(entry_in_db, space.embedding_models)
        await self._set_members(entry_in_db, space.members)

        return self.factory.create_space_from_db(entry_in_db)

    async def get(self, id: UUID) -> Space:
        query = sa.select(Spaces).where(Spaces.id == id)

        return await self._get_from_query(query)

    async def get_personal_space(self, user_id: UUID) -> Space:
        query = sa.select(Spaces).where(Spaces.user_id == user_id)

        return await self._get_from_query(query)

    async def update(self, space: Space) -> Space:
        query = (
            sa.update(Spaces)
            .values(name=space.name, description=space.description)
            .where(Spaces.id == space.id)
            .returning(Spaces)
        )
        entry_in_db = await self.get_record_with_options(query)

        groups = await self._get_groups(space.id)

        await self._set_completion_models(entry_in_db, space.completion_models)
        await self._set_embedding_models(entry_in_db, space.embedding_models)
        await self._set_members(entry_in_db, space.members)

        return self.factory.create_space_from_db(entry_in_db, groups_in_db=groups)

    async def delete(self, id: UUID):
        query = sa.delete(Spaces).where(Spaces.id == id)
        await self.session.execute(query)

    async def get_spaces(self, user_id: UUID) -> list[Space]:
        query = (
            sa.select(Spaces)
            .join(SpacesUsers, Spaces.members)
            .where(SpacesUsers.user_id == user_id)
            .distinct()
            .order_by(Spaces.created_at)
        )

        records = await self.get_records_with_options(query)

        return [self.factory.create_space_from_db(record) for record in records]
