from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.info_blobs import info_blob_protocol
from instorage.info_blobs.info_blob import InfoBlobPublicNoText
from instorage.main.container.container import Container
from instorage.main.models import PaginatedResponse
from instorage.server import protocol
from instorage.server.dependencies.container import get_container
from instorage.server.protocol import responses, to_paginated_response
from instorage.spaces.api.space_models import TransferRequest
from instorage.websites.crawl_dependencies.crawl_models import CrawlRunPublic
from instorage.websites.website_factory import get_website_service
from instorage.websites.website_models import (
    WebsiteCreateRequest,
    WebsitePublic,
    WebsiteUpdateRequest,
)
from instorage.websites.website_service import WebsiteService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[WebsitePublic])
async def get_websites(
    for_tenant: bool = False, service: WebsiteService = Depends(get_website_service)
):
    crawls = await service.get_websites(by_tenant=for_tenant)

    return to_paginated_response(crawls)


@router.post("/", response_model=WebsitePublic)
async def create_website(
    crawl: WebsiteCreateRequest, service: WebsiteService = Depends(get_website_service)
):
    """If `crawl_type` is `sitemap`, `allowed_path` and `download_files` must be unset."""
    return await service.create_website(crawl)


@router.get(
    "/{id}/", response_model=WebsitePublic, responses=responses.get_responses([404])
)
async def get_website(id: UUID, service: WebsiteService = Depends(get_website_service)):
    return await service.get_website(id)


@router.post(
    "/{id}/", response_model=WebsitePublic, responses=responses.get_responses([404])
)
async def update_website(
    id: UUID,
    crawl: WebsiteUpdateRequest,
    service: WebsiteService = Depends(get_website_service),
):
    return await service.update_website(website_id=id, website_update_req=crawl)


@router.delete(
    "/{id}/", response_model=WebsitePublic, responses=responses.get_responses([404])
)
async def delete_website(
    id: UUID,
    service: WebsiteService = Depends(get_website_service),
):
    return await service.delete_website(id)


@router.get("/{id}/runs/", response_model=PaginatedResponse[CrawlRunPublic])
async def get_crawl_runs(
    id: UUID, service: WebsiteService = Depends(get_website_service)
):
    crawl_runs = await service.get_crawl_runs(id)

    return to_paginated_response(crawl_runs)


@router.post("/{id}/transfer/", status_code=204)
async def transfer_website_to_space(
    id: UUID,
    transfer_req: TransferRequest,
    service: WebsiteService = Depends(get_website_service),
):
    await service.move_website_to_space(
        website_id=id, space_id=transfer_req.target_space_id
    )


@router.get(
    "/{id}/info-blobs/",
    response_model=PaginatedResponse[InfoBlobPublicNoText],
    responses=responses.get_responses([400, 404]),
)
async def get_info_blobs(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.info_blob_service()

    info_blobs_in_db = await service.get_by_website(id)

    info_blobs_public = [
        info_blob_protocol.to_info_blob_public_no_text(blob)
        for blob in info_blobs_in_db
    ]

    return protocol.to_paginated_response(info_blobs_public)
