from fastapi import APIRouter, Depends

from instorage.authentication import auth_dependencies
from instorage.main.models import PaginatedResponse
from instorage.modules.module import ModuleBase, ModuleId, ModuleInDB
from instorage.modules.module_factory import get_module_repo
from instorage.modules.module_repo import ModuleRepository
from instorage.server import protocol
from instorage.tenants import tenant_factory
from instorage.tenants.tenant import TenantInDB
from instorage.tenants.tenant_service import TenantService

router = APIRouter(
    dependencies=[Depends(auth_dependencies.authenticate_super_duper_api_key)]
)


@router.get("/", response_model=PaginatedResponse[ModuleInDB])
async def get_modules(module_repo: ModuleRepository = Depends(get_module_repo)):
    modules = await module_repo.get_all_modules()

    return protocol.to_paginated_response(modules)


@router.post("/", response_model=ModuleInDB)
async def add_module(
    module: ModuleBase, module_repo: ModuleRepository = Depends(get_module_repo)
):
    return await module_repo.add(module)


@router.post("/{tenant_id}/", response_model=TenantInDB)
async def add_module_to_tenant(
    tenant_id: int,
    module_ids: list[ModuleId],
    tenant_service: TenantService = Depends(tenant_factory.get_tenant_service),
):
    """Value is a list of module `id`'s to add to the `tenant_id`."""

    return await tenant_service.add_modules(
        tenant_id=tenant_id, list_of_module_ids=module_ids
    )
