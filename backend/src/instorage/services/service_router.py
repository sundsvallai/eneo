from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.main.models import PaginatedResponse
from instorage.server.protocol import responses
from instorage.services.service import (
    RunService,
    ServiceCreatePublic,
    ServiceOutput,
    ServicePublicWithUser,
    ServiceRun,
    ServiceUpdatePublic,
)
from instorage.services.service_factory import (
    get_runner_from_service,
    get_services_service,
)
from instorage.services.service_protocol import from_domain_service, to_question
from instorage.services.service_runner import ServiceRunner
from instorage.services.service_service import ServiceService
from instorage.spaces.api.space_models import TransferApplicationRequest

router = APIRouter()


@router.post(
    "/",
    response_model=ServicePublicWithUser,
    responses=responses.get_responses([400, 404]),
)
async def create_service(
    service_model: ServiceCreatePublic,
    service: ServiceService = Depends(get_services_service),
):
    """Create a service.

    `json_schema` is required if `output_validation` is 'json'.

    Conversely, `json_schema` is not evaluated if `output_format` is not 'json'.

    if `output_format` is omitted, the output will not be formatted."""
    service_in_db = await service.create_service(service_model)

    return from_domain_service(service_in_db)


@router.get("/", response_model=PaginatedResponse[ServicePublicWithUser])
async def get_services(
    name: str = None, service: ServiceService = Depends(get_services_service)
):
    services = await service.get_services(name)

    return {
        "count": len(services),
        "items": [from_domain_service(service) for service in services],
    }


@router.get(
    "/{id}/",
    response_model=ServicePublicWithUser,
    responses=responses.get_responses([404]),
)
async def get_service(id: str, service: ServiceService = Depends(get_services_service)):
    return from_domain_service(await service.get_service(id))


@router.post(
    "/{id}/",
    response_model=ServicePublicWithUser,
    responses=responses.get_responses([404]),
)
async def update_service(
    id: str,
    service_model: ServiceUpdatePublic,
    service: ServiceService = Depends(get_services_service),
):
    """Omitted fields are not updated"""

    service = await service.update_service(service_model, id)

    return from_domain_service(service)


@router.delete(
    "/{id}/",
    status_code=204,
    responses=responses.get_responses([403, 404]),
)
async def delete_service(
    id: str, service: ServiceService = Depends(get_services_service)
):
    await service.delete_service(id)


@router.post(
    "/{id}/run/",
    response_model=ServiceOutput,
    responses=responses.get_responses([404, 400]),
)
async def run_service(
    input: RunService, service_runner: ServiceRunner = Depends(get_runner_from_service)
):
    """The schema of the output will be depending on the output validation of the service"""
    output = await service_runner.run(input.input)

    return ServiceOutput(output=output.result)


@router.get(
    "/{id}/run/",
    response_model=PaginatedResponse[ServiceRun],
    responses=responses.get_responses([404]),
)
async def get_service_runs(
    id: str, service: ServiceService = Depends(get_services_service)
):
    service, runs = await service.get_service_runs(id)

    return {
        "count": len(runs),
        "items": [to_question(run, service) for run in runs],
    }


@router.post("/{id}/transfer/", status_code=204)
async def transfer_service_to_space(
    id: UUID,
    transfer_req: TransferApplicationRequest,
    service: ServiceService = Depends(get_services_service),
):
    await service.move_service_to_space(
        service_id=id,
        space_id=transfer_req.target_space_id,
        move_resources=transfer_req.move_resources,
    )
