from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from instorage.main.exceptions import NotFoundException, UnauthorizedException
from instorage.websites.crawl_dependencies.crawl_models import CrawlType
from instorage.websites.website_models import UpdateInterval, WebsiteCreate
from instorage.websites.website_service import WebsiteService


@pytest.fixture
def service():
    user = MagicMock(permissions={"websites"}, tenant_id=uuid4(), id=uuid4())

    return WebsiteService(
        user=user,
        repo=AsyncMock(),
        crawl_run_repo=AsyncMock(),
        task_service=AsyncMock(),
        space_service=AsyncMock(),
        ai_models_service=AsyncMock(),
    )


async def test_update_space_website_can_not_read(service: WebsiteService):
    space = MagicMock()
    space.can_read_resource.return_value = False
    service.space_service.get_space.return_value = space

    service.repo.update.return_value = MagicMock(tenant_id=service.user.tenant_id)
    with pytest.raises(NotFoundException):
        await service.update_website(MagicMock(), uuid4())


async def test_update_space_website_can_not_edit(service: WebsiteService):
    space = MagicMock()
    space.can_edit_resource.return_value = False
    service.space_service.get_space.return_value = space

    service.repo.update.return_value = MagicMock(tenant_id=service.user.tenant_id)
    with pytest.raises(UnauthorizedException):
        await service.update_website(MagicMock(), uuid4())


async def test_update_space_website(service: WebsiteService):
    space = MagicMock()
    space.can_edit_resource.return_value = True
    service.space_service.get_space.return_value = space

    service.repo.update.return_value = MagicMock(tenant_id=service.user.tenant_id)
    await service.update_website(MagicMock(), uuid4())


async def test_delete_space_website_can_not_read(service: WebsiteService):
    space = MagicMock()
    space.can_read_resource.return_value = False
    service.space_service.get_space.return_value = space

    service.repo.get.return_value = MagicMock(tenant_id=service.user.tenant_id)
    with pytest.raises(NotFoundException):
        await service.delete_website("UUID")


async def test_delete_space_website_can_not_delete(service: WebsiteService):
    space = MagicMock()
    space.can_delete_resource.return_value = False
    service.space_service.get_space.return_value = space

    service.repo.get.return_value = MagicMock(tenant_id=service.user.tenant_id)
    with pytest.raises(UnauthorizedException):
        await service.delete_website("UUID")


async def test_delete_space_group(service: WebsiteService):
    space = MagicMock()
    space.can_delete_resource.return_value = True
    service.space_service.get_space.return_value = space

    service.repo.get.return_value = MagicMock(tenant_id=service.user.tenant_id)
    await service.delete_website("UUID")


async def test_name_is_without_protocol(service: WebsiteService):
    url = "https://www.example.com"
    name = "www.example.com"
    expected_website_create = WebsiteCreate(
        name=name,
        url=url,
        user_id=uuid4(),
        tenant_id=uuid4(),
        embedding_model_id=uuid4(),
    )

    service.repo.add.return_value = MagicMock(id=uuid4())
    service.crawl_run_repo.add.return_value = MagicMock(id=uuid4())
    service.task_service.queue_crawl.return_value = MagicMock(id=uuid4())

    await service.create_space_website(
        url=url,
        space_id=uuid4(),
        download_files=True,
        crawl_type=CrawlType.CRAWL,
        update_interval=UpdateInterval.NEVER,
        embedding_model_id=uuid4(),
    )

    assert service.repo.add.awaited_with(expected_website_create)
