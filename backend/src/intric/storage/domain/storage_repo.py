# Copyright (c) 2025 Sundsvalls Kommun
#
# Licensed under the MIT License.


from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from intric.database.database import AsyncSession
from intric.database.tables.groups_table import Groups
from intric.database.tables.spaces_table import Spaces, SpacesUsers
from intric.database.tables.tenant_table import Tenants
from intric.database.tables.websites_table import Websites
from intric.storage.domain.storage_factory import (
    StorageInfoFactory,
    StorageInfoQueryResult,
)
from intric.users.user import UserInDB

if TYPE_CHECKING:
    from intric.storage.domain.storage import StorageInfo


class StorageInfoRepository:
    def __init__(
        self, user: UserInDB, session: AsyncSession, factory: StorageInfoFactory
    ):
        self.user = user
        self.session = session
        self.factory = factory

    async def _get_spaces(self):
        tenant_id = self.user.tenant_id
        # Aliases for subqueries
        group_size_subquery = (
            sa.select(
                Groups.space_id, sa.func.sum(Groups.size).label("total_groups_size")
            )
            .group_by(Groups.space_id)
            .alias("group_size_subquery")
        )

        website_size_subquery = (
            sa.select(
                Websites.space_id,
                sa.func.sum(Websites.size).label("total_website_size"),
            )
            .group_by(Websites.space_id)
            .alias("website_size_subquery")
        )

        # Main query
        query = (
            sa.select(
                Spaces,
                sa.func.coalesce(group_size_subquery.c.total_groups_size, 0).label(
                    "total_groups_size"
                ),
                sa.func.coalesce(website_size_subquery.c.total_website_size, 0).label(
                    "total_website_size"
                ),
                Tenants.quota_limit,
            )
            .outerjoin(group_size_subquery, Spaces.id == group_size_subquery.c.space_id)
            .outerjoin(
                website_size_subquery, Spaces.id == website_size_subquery.c.space_id
            )
            .join(Tenants, Spaces.tenant_id == Tenants.id)
            .where(Spaces.tenant_id == tenant_id)
            .options(selectinload(Spaces.members).selectinload(SpacesUsers.user))
        )

        return await self.session.execute(query)

    async def get_storage_info(self) -> "StorageInfo":

        results = await self._get_spaces()
        result = results.mappings().all()

        storage_info_list = [
            StorageInfoQueryResult(
                spaces=row["Spaces"],
                group_size=row["total_groups_size"],
                website_size=row["total_website_size"],
                total_size=row["total_groups_size"] + row["total_website_size"],
                quota_limit=row["quota_limit"],
            )
            for row in result
        ]

        storage_info = self.factory.create_storage_info_from_db(
            query_result=storage_info_list
        )
        return storage_info
