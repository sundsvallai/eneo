from fastapi import APIRouter, Depends

from instorage.allowed_origins.allowed_origin_factory import get_allowed_origins_service
from instorage.allowed_origins.allowed_origin_models import AllowedOriginPublic
from instorage.allowed_origins.allowed_origin_service import AllowedOriginService
from instorage.main.models import PaginatedResponse
from instorage.server import protocol

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[AllowedOriginPublic])
async def get_origins(
    service: AllowedOriginService = Depends(get_allowed_origins_service),
):
    allowed_origins = await service.get()

    return protocol.to_paginated_response(allowed_origins)
