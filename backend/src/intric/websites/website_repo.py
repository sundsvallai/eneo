from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from intric.database.database import AsyncSession
from intric.database.repositories.base import BaseRepositoryDelegate
from intric.database.tables.assistant_table import AssistantsWebsites
from intric.database.tables.tenant_table import Tenants
from intric.database.tables.users_table import Users
from intric.database.tables.websites_table import CrawlRuns, Websites
from intric.database.tables.info_blobs_table import InfoBlobs
from intric.websites.website_models import Website, WebsiteCreate, WebsiteUpdate


class WebsiteRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session=session,
            table=Websites,
            in_db_model=Website,
            with_options=[
                selectinload(Websites.embedding_model),
                selectinload(Websites.latest_crawl).selectinload(CrawlRuns.job),
            ],
        )
        self.session = session

    async def add(self, website: WebsiteCreate) -> Website:
        return await self.delegate.add(website)

    async def get(self, id: UUID) -> Website:
        return await self.delegate.get(id)

    async def get_by_ids(self, ids: list[UUID]) -> list[Website]:
        return await self.delegate.get_by_ids(ids)

    async def get_by_tenant(self, tenant_id: UUID):
        stmt = (
            sa.select(Websites)
            .join(Users)
            .join(Tenants)
            .where(Tenants.id == tenant_id)
            .order_by(Websites.created_at)
        )

        return await self.delegate.get_models_from_query(stmt)

    async def get_by_user(self, user_id: UUID) -> list[Website]:
        return await self.delegate.filter_by(conditions={Websites.user_id: user_id})

    async def get_all(self) -> list[Website]:
        return await self.delegate.get_all()

    async def update(self, website: WebsiteUpdate) -> Website:
        return await self.delegate.update(website)

    async def update_website_size(self, website_id: UUID):
        info_blobs_size_subquery = (
            sa.select(sa.func.coalesce(sa.func.sum(InfoBlobs.size), 0))
            .where(InfoBlobs.website_id == website_id)
            .scalar_subquery()
        )

        stmt = (
            sa.update(Websites)
            .where(Websites.id == website_id)
            .values(size=info_blobs_size_subquery)
            .returning(Websites)
        )

        return await self.session.scalar(stmt)

    async def delete(self, id: UUID):
        return await self.delegate.delete(id)

    async def add_website_to_space(self, website_id: UUID, space_id: UUID):
        stmt = (
            sa.update(Websites)
            .where(Websites.id == website_id)
            .values(space_id=space_id)
            .returning(Websites)
        )

        return await self.delegate.get_model_from_query(stmt)

    async def set_embedding_model(self, website_id: UUID, embedding_model_id: UUID):
        stmt = (
            sa.update(Websites)
            .where(Websites.id == website_id)
            .values(embedding_model_id=embedding_model_id)
            .returning(Websites)
        )

        return await self.delegate.get_model_from_query(stmt)

    async def remove_website_from_all_assistants(
        self, website_id: UUID, assistant_ids: list[UUID]
    ):
        stmt = (
            sa.delete(AssistantsWebsites)
            .where(AssistantsWebsites.website_id == website_id)
            .where(
                AssistantsWebsites.assistant_id.not_in(assistant_ids),
            )
        )

        await self.session.execute(stmt)
