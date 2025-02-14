from unittest.mock import AsyncMock, MagicMock

import pytest

from intric.groups.api.group_models import GroupUpdatePublic
from intric.groups.group_service import GroupService
from intric.main.exceptions import UnauthorizedException
from tests.fixtures import TEST_USER, TEST_UUID


@pytest.fixture
def service():
    repo = AsyncMock()
    tenant_repo = AsyncMock()
    info_blob_repo = AsyncMock()
    space_repo = AsyncMock()
    space_repo.get_space_by_group.return_value = MagicMock()

    return GroupService(
        user=TEST_USER,
        repo=repo,
        space_repo=space_repo,
        tenant_repo=tenant_repo,
        info_blob_repo=info_blob_repo,
        ai_models_service=AsyncMock(),
        space_service=AsyncMock(),
        actor_manager=MagicMock(),
        task_service=AsyncMock(),
    )


async def test_update_space_group_not_member(service: GroupService):
    group_update = GroupUpdatePublic(name="new name")

    actor = MagicMock()
    actor.can_edit_groups.return_value = False
    service.actor_manager.get_space_actor_from_space.return_value = actor

    with pytest.raises(UnauthorizedException):
        await service.update_group(group_update, TEST_UUID)


async def test_update_space_group_member(service: GroupService):
    group_update = GroupUpdatePublic(name="new name")

    await service.update_group(group_update, TEST_UUID)


async def test_delete_space_group_not_member(service: GroupService):
    actor = MagicMock()
    actor.can_delete_groups.return_value = False
    service.actor_manager.get_space_actor_from_space.return_value = actor

    with pytest.raises(UnauthorizedException):
        await service.delete_group(TEST_UUID)


async def test_delete_space_group_member(service: GroupService):
    await service.delete_group(TEST_UUID)
