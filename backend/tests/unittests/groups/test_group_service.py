from copy import deepcopy
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from instorage.groups.group import GroupUpdatePublic
from instorage.groups.group_service import GroupService
from instorage.main.exceptions import NotFoundException, UnauthorizedException
from instorage.roles.permissions import Permission
from instorage.roles.role import RoleInDB
from tests.fixtures import TEST_GROUP, TEST_USER, TEST_UUID


@pytest.fixture
def service():
    repo = AsyncMock()
    tenant_repo = AsyncMock()
    info_blob_repo = AsyncMock()

    return GroupService(
        user=TEST_USER,
        repo=repo,
        tenant_repo=tenant_repo,
        info_blob_repo=info_blob_repo,
        ai_models_service=AsyncMock(),
        space_service=AsyncMock(),
    )


async def test_get_exception_with_nonexistant_group(service: GroupService):
    service.repo.get_group.return_value = None
    service.repo.update_group.return_value = None
    service.repo.delete_group_by_id.return_value = None

    group_update = GroupUpdatePublic(name="new_name")

    with pytest.raises(NotFoundException, match="not found"):
        await service.get_group(1)

    with pytest.raises(NotFoundException, match="not found"):
        await service.update_group(group_update, id=uuid4())

    with pytest.raises(NotFoundException, match="not found"):
        await service.delete_group(1)


async def test_set_can_edit(service: GroupService):
    user = deepcopy(TEST_USER)
    group = deepcopy(TEST_GROUP)

    user.roles = [
        RoleInDB(
            id=uuid4(),
            name="role1",
            permissions=[Permission.EDITOR],
            tenant_id=uuid4(),
        ),
        RoleInDB(
            id=uuid4(),
            name="role2",
            permissions=[Permission.EDITOR],
            tenant_id=uuid4(),
        ),
    ]
    user.id = 2

    # Assert different user
    service.user = user
    assert service.user.id != group.user.id

    service.repo.get_all_groups.return_value = [group]

    groups = await service.get_groups_for_user()

    assert groups[0].can_edit
    assert groups[0].user_id != user.id


async def test_update_space_group_not_member(service: GroupService):
    group_update = GroupUpdatePublic(name="new name")

    space = MagicMock()
    space.can_edit_resource.return_value = False
    service.space_service.get_space.return_value = space

    with pytest.raises(UnauthorizedException):
        await service.update_group(group_update, TEST_UUID)


async def test_update_space_group_member(service: GroupService):
    group_update = GroupUpdatePublic(name="new name")

    space = MagicMock()
    space.can_edit_resource.return_value = True
    service.space_service.get_space.return_value = space

    await service.update_group(group_update, TEST_UUID)


async def test_delete_space_group_not_member(service: GroupService):
    space = MagicMock()
    space.can_delete_resource.return_value = False
    service.space_service.get_space.return_value = space

    with pytest.raises(UnauthorizedException):
        await service.delete_group(TEST_UUID)


async def test_delete_space_group_member(service: GroupService):
    space = MagicMock()
    space.can_delete_resource.return_value = True
    service.space_service.get_space.return_value = space

    await service.delete_group(TEST_UUID)
