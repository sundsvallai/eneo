from fastapi import APIRouter, Depends

from intric.main.container.container import Container
from intric.server.dependencies.container import get_container
from intric.integration.presentation.models import (
    IntegrationList,
    TenantIntegrationList,
    UserIntegrationList,
)


router = APIRouter()


@router.get(
    "/",
    response_model=IntegrationList,
    status_code=200,
)
async def get_integrations(
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.integration_service()

    integrations = await service.get_integrations()

    assembler = container.integration_assembler()

    return assembler.to_paginated_response(integrations=integrations)


@router.get(
    "/tenant/",
    response_model=TenantIntegrationList,
    status_code=200,
)
async def get_tenant_integrations(
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.tenant_integration_service()

    user = container.user()

    tenant_integrations = await service.get_tenant_integrations(
        tenant_id=user.tenant_id
    )
    assembler = container.tenant_integration_assembler()
    return assembler.to_paginated_response(integrations=tenant_integrations)


@router.get(
    "/me/",
    response_model=UserIntegrationList,
    status_code=200,
)
async def get_user_integrations(
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.user_integration_service()
    user = container.user()
    user_integrations = await service.get_user_integrations(user_id=user.id)

    assembler = container.user_integration_assembler()
    return assembler.to_paginated_response(integrations=user_integrations)
