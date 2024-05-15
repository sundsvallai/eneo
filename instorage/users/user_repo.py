from datetime import datetime, timezone
from uuid import UUID

import sqlalchemy as sa
from pydantic import EmailStr
from sqlalchemy.orm import selectinload

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.roles_table import PredefinedRoles, Roles
from instorage.database.tables.tenant_table import Tenants
from instorage.database.tables.users_table import Users
from instorage.database.tables.widget_table import Widgets
from instorage.main.models import ModelUUID
from instorage.users.user import UserAdd, UserInDB, UserUpdate


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            Users,
            UserInDB,
            with_options=self._get_options(),
        )
        self.session = session

    def _get_options(self):
        return [
            selectinload(Users.roles),
            selectinload(Users.predefined_roles),
            selectinload(Users.tenant).selectinload(Tenants.modules),
            selectinload(Users.api_key),
            selectinload(Users.user_groups),
        ]

    async def _get_model_from_query(self, query, with_deleted: bool = False):
        if not with_deleted:
            query = query.where(Users.deleted_at.is_(None))

        return await self.delegate.get_model_from_query(query)

    async def _get_models_from_query(self, query, with_deleted: bool = False):
        if not with_deleted:
            query = query.where(Users.deleted_at.is_(None))

        return await self.delegate.get_models_from_query(query)

    async def get_user_by_email(
        self, email: EmailStr, with_deleted: bool = False
    ) -> UserInDB:
        query = sa.select(Users).where(Users.email == email)

        return await self._get_model_from_query(query, with_deleted=with_deleted)

    async def get_user_by_username(
        self, username: str, with_deleted: bool = False
    ) -> UserInDB:
        query = sa.select(Users).where(Users.username == username)

        return await self._get_model_from_query(query, with_deleted=with_deleted)

    async def get_user_by_id(self, id: int, with_deleted: bool = False) -> UserInDB:
        query = sa.select(Users).where(Users.id == id)

        return await self._get_model_from_query(query, with_deleted=with_deleted)

    async def get_user_by_uuid(self, id: UUID, with_deleted: bool = False) -> UserInDB:
        query = sa.select(Users).where(Users.uuid == id)

        return await self._get_model_from_query(query, with_deleted=with_deleted)

    async def get_user_by_widget_id(self, widget_id: int) -> UserInDB:
        query = sa.select(Users).join(Widgets).where(Widgets.id == widget_id)
        return await self.delegate.get_model_from_query(query)

    async def get_all_users(self, tenant_id: int = None, with_deleted: bool = False):
        query = sa.select(Users).order_by(Users.created_at)

        if tenant_id is not None:
            query = query.where(Users.tenant_id == tenant_id)

        return await self._get_models_from_query(query, with_deleted=with_deleted)

    async def _get_roles(self, roles: list[ModelUUID] | None):
        if roles is None:
            return []

        roles_ids = [role.id for role in roles]
        stmt = sa.select(Roles).filter(Roles.uuid.in_(roles_ids))
        roles = await self.session.scalars(stmt)

        return roles.all()

    async def _get_predefined_roles(self, roles: list[ModelUUID] | None):
        if roles is None:
            return []

        roles_ids = [role.id for role in roles]
        stmt = sa.select(PredefinedRoles).filter(PredefinedRoles.id.in_(roles_ids))
        roles = await self.session.scalars(stmt)

        return roles.all()

    async def add(self, user: UserAdd):
        stmt = (
            sa.insert(Users)
            .values(
                **user.model_dump(
                    exclude_none=True, exclude={"roles", "predefined_roles"}
                )
            )
            .returning(Users)
        )
        entry_in_db = await self.delegate.get_record_from_query(query=stmt)
        # TODO should be refactored when we will remove int id field from tables
        entry_in_db.roles = await self._get_roles(user.roles)
        entry_in_db.predefined_roles = await self._get_predefined_roles(
            user.predefined_roles
        )

        return UserInDB.model_validate(entry_in_db)

    async def update(self, user: UserUpdate):
        stmt = (
            sa.update(Users)
            .values(
                **user.model_dump(
                    exclude_unset=True, exclude={"id", "roles", "predefined_roles"}
                )
            )
            .where(Users.id == user.id)
            .returning(Users)
        )
        entry_in_db = await self.delegate.get_record_from_query(query=stmt)

        if entry_in_db is None:
            return

        # TODO should be refactored when we will remove int id field from tables
        if "roles" in user.model_dump(exclude_unset=True):
            entry_in_db.roles = await self._get_roles(user.roles)

        if "predefined_roles" in user.model_dump(exclude_unset=True):
            entry_in_db.predefined_roles = await self._get_predefined_roles(
                user.predefined_roles
            )

        return UserInDB.model_validate(entry_in_db)

    async def hard_delete(self, id: int):
        return await self.delegate.delete(id)

    async def soft_delete(self, id: int):
        stmt = (
            sa.update(Users)
            .values(deleted_at=datetime.now(timezone.utc))
            .where(Users.id == id)
            .returning(Users)
        )
        return await self.delegate.get_model_from_query(stmt)

    async def delete(self, id: int, soft_delete: bool = True):
        if soft_delete:
            return await self.soft_delete(id=id)
        return await self.hard_delete(id=id)
