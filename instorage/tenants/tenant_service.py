from typing import List

from instorage.main.exceptions import NotFoundException
from instorage.modules.module import ModuleId
from instorage.tenants.tenant import (
    TenantBase,
    TenantInDB,
    TenantUpdate,
    TenantUpdatePublic,
)
from instorage.tenants.tenant_repo import TenantRepository


class TenantService:
    def __init__(
        self,
        repo: TenantRepository,
    ):
        self.repo = repo

    @staticmethod
    def _validate(tenant: TenantInDB, id: int):
        if not tenant:
            raise NotFoundException(f"Tenant {id} not found")

    async def get_all_tenants(self) -> List[TenantInDB]:
        return await self.repo.get_all_tenants()

    async def get_tenant_by_id(self, id: int) -> TenantInDB:
        tenant = await self.repo.get(id)
        self._validate(tenant, id)

        return tenant

    async def create_tenant(self, tenant: TenantBase) -> TenantInDB:
        return await self.repo.add(tenant)

    async def delete_tenant(self, tenant_id: int) -> TenantInDB:
        tenant = await self.get_tenant_by_id(tenant_id)
        self._validate(tenant, tenant_id)

        return await self.repo.delete_tenant_by_id(tenant_id)

    async def update_tenant(
        self, tenant_update: TenantUpdatePublic, id: int
    ) -> TenantInDB:
        tenant = await self.get_tenant_by_id(id)
        self._validate(tenant, id)

        tenant_update = TenantUpdate(
            **tenant_update.model_dump(exclude_unset=True), id=tenant.id
        )
        return await self.repo.update_tenant(tenant_update)

    async def add_modules(self, list_of_module_ids: list[ModuleId], tenant_id: int):
        return await self.repo.add_modules(list_of_module_ids, tenant_id)
