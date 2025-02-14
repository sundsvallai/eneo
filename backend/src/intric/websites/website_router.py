from uuid import UUID

from fastapi import APIRouter, Depends

from intric.info_blobs import info_blob_protocol
from intric.info_blobs.info_blob import InfoBlobPublicNoText
from intric.main.container.container import Container
from intric.main.models import PaginatedResponse
from intric.server import protocol
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses, to_paginated_response
from intric.spaces.api.space_models import TransferRequest
from intric.websites.crawl_dependencies.crawl_models import CrawlRunPublic
from intric.websites.website_models import (
    WebsiteCreateRequest,
    WebsitePublic,
    WebsiteUpdateRequest,
)

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[WebsitePublic])
async def get_websites(
    for_tenant: bool = False,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.website_service()
    crawls = await service.get_websites(by_tenant=for_tenant)

    return to_paginated_response(crawls)


@router.post("/", response_model=WebsitePublic, deprecated=True)
async def create_website(
    crawl: WebsiteCreateRequest,
    container: Container = Depends(get_container(with_user=True)),
):
    """If `crawl_type` is `sitemap`, `allowed_path` and `download_files` must be unset."""
    service = container.website_service()
    assembler = container.website_assembler()
    website = await service.create_website(crawl)
    return assembler.from_website_to_model(website=website)


@router.get(
    "/{id}/", response_model=WebsitePublic, responses=responses.get_responses([404])
)
async def get_website(
    id: UUID, container: Container = Depends(get_container(with_user=True))
):
    service = container.website_service()
    assembler = container.website_assembler()
    website = await service.get_website(id)
    return assembler.from_website_to_model(website=website)


@router.post(
    "/{id}/", response_model=WebsitePublic, responses=responses.get_responses([404])
)
async def update_website(
    id: UUID,
    crawl: WebsiteUpdateRequest,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.website_service()
    assembler = container.website_assembler()
    website = await service.update_website(website_id=id, website_update_req=crawl)
    return assembler.from_website_to_model(website=website)


@router.delete(
    "/{id}/", response_model=WebsitePublic, responses=responses.get_responses([404])
)
async def delete_website(
    id: UUID, container: Container = Depends(get_container(with_user=True))
):
    service = container.website_service()
    assembler = container.website_assembler()
    website = await service.delete_website(id)
    return assembler.from_website_to_model(website=website)


@router.post(
    "/{id}/run/",
    response_model=CrawlRunPublic,
    responses=responses.get_responses([403, 404]),
)
async def run_crawl(
    id: UUID, container: Container = Depends(get_container(with_user=True))
):
    # MIT License

    service = container.website_service()
    crawl_run = await service.crawl_website(id)

    return crawl_run


@router.get("/{id}/runs/", response_model=PaginatedResponse[CrawlRunPublic])
async def get_crawl_runs(
    id: UUID, container: Container = Depends(get_container(with_user=True))
):
    service = container.website_service()
    crawl_runs = await service.get_crawl_runs(id)

    return to_paginated_response(crawl_runs)


@router.post("/{id}/transfer/", status_code=204)
async def transfer_website_to_space(
    id: UUID,
    transfer_req: TransferRequest,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.website_service()
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
