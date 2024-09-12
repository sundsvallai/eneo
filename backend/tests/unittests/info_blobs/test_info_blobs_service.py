from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock

import pytest

from instorage.groups.group_service import GroupService
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.info_blobs.info_blob_service import InfoBlobService
from instorage.main.exceptions import NameCollisionException, NotFoundException
from instorage.spaces.space import SpacePermissionsActions


@dataclass
class Setup:
    repo: InfoBlobRepository
    service: InfoBlobService
    group_service: GroupService


@pytest.fixture
def setup():
    repo = AsyncMock()
    group_service = AsyncMock()

    service = InfoBlobService(
        repo=repo,
        user=MagicMock(),
        quota_service=AsyncMock(),
        group_service=group_service,
        website_service=AsyncMock(),
    )

    setup = Setup(repo=repo, service=service, group_service=group_service)

    return setup


async def test_get_info_blob_does_not_exist(setup: Setup):
    setup.repo.get.return_value = None

    with pytest.raises(NotFoundException, match="InfoBlob not found"):
        await setup.service.get_by_id("non-existant id 1")


async def test_update_info_blob_does_not_exist(setup: Setup):
    setup.repo.update.return_value = None
    setup.repo.get_by_title_and_group.return_value = None

    with pytest.raises(NotFoundException, match="InfoBlob not found"):
        await setup.service.update_info_blob(MagicMock())


async def test_delete_info_blob_does_not_exist(setup: Setup):
    setup.repo.delete.return_value = None

    with pytest.raises(NotFoundException, match="InfoBlob not found"):
        await setup.service.delete("UUID")


async def test_get_info_blob_permissions_check(setup: Setup):
    group = MagicMock(space_id=None)
    setup.group_service.get_group.return_value = group

    await setup.service.get_by_id(1)
    setup.group_service.get_group.assert_awaited_once()
    setup.group_service.check_permissions.assert_awaited_once_with(
        group=group, action=SpacePermissionsActions.READ
    )


async def test_update_info_blob_permissions_check(setup: Setup):
    group = MagicMock(space_id=None)
    setup.group_service.get_group.return_value = group

    setup.repo.get_by_title_and_group.return_value = None
    await setup.service.update_info_blob(MagicMock())

    setup.group_service.get_group.assert_awaited_once()
    setup.group_service.check_permissions.assert_awaited_once_with(
        group=group, action=SpacePermissionsActions.EDIT
    )


async def test_delete_info_blob_permissions_check(setup: Setup):
    group = MagicMock(space_id=None)
    setup.group_service.get_group.return_value = group

    await setup.service.delete("UUID")

    setup.group_service.get_group.assert_awaited_once()
    setup.group_service.check_permissions.assert_awaited_once_with(
        group=group, action=SpacePermissionsActions.DELETE
    )


async def test_get_by_user_empty_list_when_no_info_blobs(setup: Setup):
    info_blobs_by_user = await setup.service.get_by_user()

    assert info_blobs_by_user == []


async def test_update_fails_if_info_blob_with_same_name_exists(setup: Setup):
    setup.repo.get_by_title_and_group.return_value = MagicMock()

    with pytest.raises(NameCollisionException):
        await setup.service.update_info_blob(MagicMock())
