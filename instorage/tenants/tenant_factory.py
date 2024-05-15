from fastapi import Depends

from instorage.server.dependencies.db import get_repository
from instorage.tenants.tenant_repo import TenantRepository
from instorage.tenants.tenant_service import TenantService


def get_tenant_service(
    tenant_repo: TenantRepository = Depends(get_repository(TenantRepository)),
):
    return TenantService(repo=tenant_repo)
