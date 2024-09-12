from fastapi import APIRouter, Depends

from instorage.dashboard.api.dashboard_models import Dashboard
from instorage.main.container.container import Container
from instorage.server import protocol
from instorage.server.dependencies.container import get_container

router = APIRouter()


@router.get("/", response_model=Dashboard)
async def get_dashboard(container: Container = Depends(get_container(with_user=True))):
    space_service = container.space_service()
    assembler = container.space_assembler()

    spaces = await space_service.get_spaces(include_personal=True)

    space_models = [assembler.from_space_to_model(space) for space in spaces]

    return Dashboard(spaces=protocol.to_paginated_response(space_models))
