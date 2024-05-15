# MIT License

from typing import List
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import (
    BaseRepositoryDelegate,
    RelationshipOption,
)
from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.service_table import Services
from instorage.database.tables.tenant_table import Tenants
from instorage.database.tables.user_groups_table import UserGroups
from instorage.database.tables.users_table import Users
from instorage.main.exceptions import UniqueException
from instorage.user_groups.user_group import (
    UserGroupCreate,
    UserGroupInDB,
    UserGroupUpdate,
)


class UserGroupsRepository:
    UNIQUE_EXCEPTION_MSG = "User group name already exists."

    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            UserGroups,
            UserGroupInDB,
            with_options=self._get_options(),
        )

    def _get_options(self):
        return [
            selectinload(UserGroups.users).selectinload(Users.roles),
            selectinload(UserGroups.users).selectinload(Users.predefined_roles),
            selectinload(UserGroups.users)
            .selectinload(Users.tenant)
            .selectinload(Tenants.modules),
            selectinload(UserGroups.users).selectinload(Users.api_key),
            selectinload(UserGroups.assistants).selectinload(Assistants.user),
            selectinload(UserGroups.services).selectinload(Services.user),
            selectinload(UserGroups.groups),
            selectinload(UserGroups.groups).selectinload(Groups.user_groups),
        ]

    async def get_user_group_by_uuid(self, uuid: UUID) -> UserGroupInDB:
        return await self.delegate.get_by(conditions={UserGroups.uuid: uuid})

    async def create_user_group(self, user_group: UserGroupCreate) -> UserGroupInDB:
        try:
            return await self.delegate.add(user_group)
        except IntegrityError as e:
            raise UniqueException(self.UNIQUE_EXCEPTION_MSG) from e

    @staticmethod
    def _get_relationship_options():
        return [
            RelationshipOption(
                name="users",
                table=Users,
                options=[
                    selectinload(Users.roles),
                    selectinload(Users.predefined_roles),
                    selectinload(Users.tenant).selectinload(Tenants.modules),
                    selectinload(Users.api_key),
                ],
            ),
            RelationshipOption(
                name="assistants",
                table=Assistants,
                options=[selectinload(Assistants.user)],
            ),
            RelationshipOption(
                name="services",
                table=Services,
                options=[selectinload(Services.user)],
            ),
            RelationshipOption(
                name="groups",
                table=Groups,
                options=[selectinload(Groups.user_groups)],
            ),
        ]

    async def update_user_group(self, user_group: UserGroupUpdate) -> UserGroupInDB:
        try:
            return await self.delegate.update(
                user_group,
                relationships=self._get_relationship_options(),
            )

        except IntegrityError as e:
            raise UniqueException(self.UNIQUE_EXCEPTION_MSG) from e

    async def delete_user_group_by_uuid(self, uuid: UUID) -> UserGroupInDB:
        return await self.delegate.delete_by_uuid(uuid)

    async def get_all_user_groups(self, tenant_id: int = None) -> List[UserGroupInDB]:
        return await self.delegate.filter_by(
            conditions={UserGroups.tenant_id: tenant_id}
        )
