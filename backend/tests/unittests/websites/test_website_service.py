from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from intric.main.exceptions import UnauthorizedException
from intric.websites.crawl_dependencies.crawl_models import CrawlType
from intric.websites.website_models import UpdateInterval, WebsiteCreate
from intric.websites.website_service import WebsiteService


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
        actor_manager=MagicMock(),
    )


async def test_read_space_website_can_not_read(service: WebsiteService):
    actor = MagicMock()
    actor.can_read_websites.return_value = False
    service.actor_manager.get_space_actor_from_space.return_value = actor

    service.repo.get.return_value = MagicMock(tenant_id=service.user.tenant_id)

    with pytest.raises(UnauthorizedException):
        await service.get_website(MagicMock())


async def test_update_space_website_can_not_edit(service: WebsiteService):
    actor = MagicMock()
    actor.can_edit_websites.return_value = False
    service.actor_manager.get_space_actor_from_space.return_value = actor

    service.repo.update.return_value = MagicMock(tenant_id=service.user.tenant_id)
    with pytest.raises(UnauthorizedException):
        await service.update_website(MagicMock(), uuid4())


async def test_update_space_website(service: WebsiteService):
    service.repo.update.return_value = MagicMock(tenant_id=service.user.tenant_id)
    await service.update_website(MagicMock(), uuid4())


async def test_delete_space_website_can_not_delete(service: WebsiteService):
    actor = MagicMock()
    actor.can_delete_websites.return_value = False
    service.actor_manager.get_space_actor_from_space.return_value = actor

    service.repo.get.return_value = MagicMock(tenant_id=service.user.tenant_id)
    with pytest.raises(UnauthorizedException):
        await service.delete_website("UUID")


async def test_delete_space_group(service: WebsiteService):
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
