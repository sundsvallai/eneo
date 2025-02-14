from uuid import UUID

from fastapi import APIRouter, Depends

from intric.apps.app_runs.api.app_run_models import AppRunPublic
from intric.main.container.container import Container
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses

router = APIRouter()


@router.get(
    "/{id}/",
    response_model=AppRunPublic,
    responses=responses.get_responses([403, 404]),
)
async def get_app_run(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.app_run_service()
    assembler = container.app_run_assembler()

    app_run = await service.get_app_run(id)

    return assembler.from_app_run_to_model(app_run)


@router.delete(
    "/{id}/",
    status_code=204,
    responses=responses.get_responses([403, 404]),
)
async def delete_app_run(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.app_run_service()

    await service.delete_app_run(id)
