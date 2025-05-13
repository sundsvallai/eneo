from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends

from intric.integration.presentation.models import (
    AuthCallbackParams,
    AuthUrlPublic,
    UserIntegration,
)
from intric.main.container.container import Container
from intric.server.dependencies.container import get_container

router = APIRouter()


@router.get(
    "/{tenant_integration_id}/url/",
    response_model=AuthUrlPublic,
    status_code=200,
)
async def gen_url(
    tenant_integration_id: UUID,
    state: Optional[str] = None,
    container: Container = Depends(get_container(with_user=True)),
):
    oauth2_service = container.oauth2_service()

    return await oauth2_service.start_auth(
        tenant_integration_id=tenant_integration_id, state=state
    )


@router.post("/callback/token/", status_code=200, response_model=UserIntegration)
async def on_auth_callback(
    params: AuthCallbackParams,
    container: Container = Depends(get_container(with_user=True)),
):
    oauth2_service = container.oauth2_service()
    user = container.user()
    assembler = container.user_integration_assembler()

    integration = await oauth2_service.auth_integration(
        user_id=user.id,
        tenant_integration_id=params.tenant_integration_id,
        auth_code=params.auth_code,
    )
    return assembler.from_domain_to_model(item=integration)
