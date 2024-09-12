from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from pydantic import HttpUrl
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.module_table import Modules
from instorage.database.tables.tenant_table import Tenants
from instorage.main import exceptions
from instorage.main.models import ModelId
from instorage.tenants.tenant import TenantBase, TenantInDB, TenantUpdate


class TenantRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            Tenants,
            TenantInDB,
            with_options=[selectinload(Tenants.modules)],
        )
        self.session = session

    async def add(self, tenant: TenantBase) -> TenantInDB:
        try:
            return await self.delegate.add(tenant)
        except IntegrityError as e:
            raise exceptions.UniqueException("Tenant name already exists.") from e

    async def get(self, id: UUID) -> TenantInDB:
        return await self.delegate.get(id)

    async def get_all_tenants(self, domain: str | None = None):
        if domain is not None:
            return await self.delegate.filter_by(conditions={Tenants.domain: domain})

        return await self.delegate.get_all()

    async def add_modules(self, list_of_module_ids: list[ModelId], tenant_id: UUID):
        module_ids = [module.id for module in list_of_module_ids]
        module_stmt = sa.select(Modules).filter(Modules.id.in_(module_ids))
        modules = await self.session.scalars(module_stmt)

        tenant_stmt = (
            sa.select(Tenants)
            .where(Tenants.id == tenant_id)
            .options(selectinload(Tenants.modules))
        )
        tenant = await self.session.scalar(tenant_stmt)

        tenant.modules = modules.all()

        return TenantInDB.model_validate(tenant)

    async def update_tenant(self, tenant: TenantUpdate) -> TenantInDB:
        return await self.delegate.update(tenant)

    async def delete_tenant_by_id(self, id: UUID) -> TenantInDB:
        return await self.delegate.delete(id)

    async def set_privacy_policy(
        self, privacy_policy: Optional[HttpUrl], tenant_id: UUID
    ) -> TenantInDB:
        privacy_policy = str(privacy_policy) if privacy_policy is not None else None
        stmt = (
            sa.update(Tenants)
            .where(Tenants.id == tenant_id)
            .values(privacy_policy=privacy_policy)
            .returning(Tenants)
            .options(selectinload(Tenants.modules))
        )

        return await self.delegate.get_model_from_query(stmt)
