from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from instorage.main.config import SETTINGS
from instorage.main.exceptions import BadRequestException, UnauthorizedException
from instorage.modules.module import Modules
from instorage.roles.permissions import Permission
from instorage.spaces.space import UNAUTHORIZED_EXCEPTION_MESSAGE, Space, SpaceRole


@pytest.fixture
def space():
    return Space(
        id=None,
        tenant_id=None,
        user_id=None,
        name=MagicMock(),
        description=None,
        embedding_models=[],
        completion_models=[],
        assistants=[],
        services=[],
        websites=[],
        groups=[],
        members={},
    )


def test_get_latest_available_embedding_model(space: Space):
    embedding_models = [
        MagicMock(created_at=datetime(2024, 1, 3 - i), can_access=True)
        for i in range(3)
    ]
    space.embedding_models = embedding_models

    embedding_model = space.get_latest_embedding_model()

    assert embedding_model == embedding_models[0]


def test_get_latest_available_embedding_model_when_not_ordered(space: Space):
    embedding_models = [
        MagicMock(created_at=datetime(2024, 1, 3 - i), can_access=True)
        for i in range(3)
    ]
    embedding_models = list(reversed(embedding_models))
    space.embedding_models = embedding_models

    embedding_model = space.get_latest_embedding_model()

    assert embedding_model == embedding_models[2]


def test_set_embedding_model_when_all_are_not_accessible(space: Space):
    embedding_models = [
        MagicMock(created_at=datetime(2024, 1, 3), can_access=False),
        MagicMock(created_at=datetime(2024, 1, 2), can_access=True),
        MagicMock(created_at=datetime(2024, 1, 1), can_access=True),
    ]

    with pytest.raises(UnauthorizedException):
        space.embedding_models = embedding_models


def test_get_space_no_access(space: Space):
    assert not space.can_read(MagicMock())


def test_get_space_admin_access(space: Space):
    admin_id = "admin_id"
    admin = MagicMock(id=admin_id, role=SpaceRole.ADMIN)
    space.members = {admin_id: admin}

    assert space.can_read(admin)


def test_get_space_editor_access(space: Space):
    editor_id = "editor_id"
    editor = MagicMock(id=editor_id, role=SpaceRole.EDITOR)
    space.members = {editor_id: editor}

    assert space.can_read(editor)


def test_space_update_embedding_model_no_acces(space: Space):
    embedding_model = MagicMock(can_access=False)

    with pytest.raises(UnauthorizedException, match=UNAUTHORIZED_EXCEPTION_MESSAGE):
        space.embedding_models = [embedding_model]


def test_space_update_embedding_models(space: Space):
    embedding_model = MagicMock(can_access=True)

    space.embedding_models = [embedding_model]

    assert space.embedding_models == [embedding_model]


def test_space_update_completion_models_no_access(space: Space):
    completion_model = MagicMock(can_access=False)

    with pytest.raises(UnauthorizedException, match=UNAUTHORIZED_EXCEPTION_MESSAGE):
        space.completion_models = [completion_model]


def test_space_update_completion_models(space: Space):
    completion_model = MagicMock(can_access=True)

    space.completion_models = [completion_model]

    assert space.completion_models == [completion_model]


def test_update_space_admin_access(space: Space):
    admin_id = "admin_id"
    admin = MagicMock(id=admin_id, role=SpaceRole.ADMIN)
    space.members = {admin_id: admin}

    assert space.can_edit(admin)


def test_update_space_editor_no_access(space: Space):
    editor_id = "editor_id"
    editor = MagicMock(id=editor_id, role=SpaceRole.EDITOR)
    space.members = {editor_id: editor}

    assert not space.can_edit(editor)


def test_delete_space_not_member(space: Space):
    assert not space.can_edit(MagicMock())


def test_get_latest_completion_model(space: Space):
    completion_models = [
        MagicMock(created_at=datetime(2024, 1, 3 - i)) for i in range(3)
    ]
    completion_models = list(reversed(completion_models))

    space.completion_models = completion_models

    assert space.get_latest_completion_model() == completion_models[2]


def test_get_latest_completion_model_none(space: Space):
    space.completion_models = []

    assert space.get_latest_completion_model() is None


def test_is_completion_model_in_space(space: Space):
    completion_model = MagicMock(id=uuid4())
    space.completion_models = [completion_model]

    assert space.is_completion_model_in_space(completion_model.id)


def test_is_completion_model_not_in_space(space: Space):
    assert not space.is_completion_model_in_space(uuid4())


def test_is_group_in_space(space: Space):
    group = MagicMock(id=uuid4())
    space.groups = [group]

    assert space.is_group_in_space(group.id)


def test_is_group_not_in_space(space: Space):
    assert not space.is_group_in_space(uuid4())


def test_is_website_in_space(space: Space):
    website = MagicMock(id=uuid4())
    space.websites = [website]

    assert space.is_website_in_space(website.id)


def test_is_website_not_in_space(space: Space):
    assert not space.is_website_in_space(uuid4())


def test_add_user_that_already_exists(space: Space):
    space.members = {"admin1": MagicMock(id="admin1", role=SpaceRole.ADMIN)}

    with pytest.raises(BadRequestException):
        space.add_member(MagicMock(id="admin1"))


def test_add_user(space: Space):
    user = MagicMock()
    space.add_member(user)

    assert user in space.members.values()


def test_remove_user(space: Space):
    space.members = {12: MagicMock()}

    space.remove_member(12)

    assert space.members == {}


def test_remove_user_if_user_does_not_exist(space: Space):
    space.members = {}

    with pytest.raises(BadRequestException):
        space.remove_member("UUID")


def test_change_role_of_user(space: Space):
    space.members = {12: MagicMock(role=SpaceRole.ADMIN)}

    space.change_member_role(12, SpaceRole.EDITOR)

    assert space.get_member(12).role == SpaceRole.EDITOR


def test_change_role_of_user_to_same(space: Space):
    space.members = {12: MagicMock(role=SpaceRole.ADMIN)}

    space.change_member_role(12, SpaceRole.ADMIN)

    assert space.get_member(12).role == SpaceRole.ADMIN


def test_change_role_of_user_if_user_not_exist(space: Space):
    space.members = {}

    with pytest.raises(BadRequestException):
        space.change_member_role("UUID", SpaceRole.ADMIN)


def test_add_member_in_personal_space(space: Space):
    space.user_id = MagicMock()

    with pytest.raises(BadRequestException):
        space.add_member(MagicMock())


def test_cannot_change_description_of_personal_space(space: Space):
    space.user_id = MagicMock()

    with pytest.raises(BadRequestException):
        space.update(description="new description")


def test_cannot_change_name_of_personal_space(space: Space):
    space.user_id = MagicMock()

    with pytest.raises(BadRequestException):
        space.update(name="new name")


def test_cannot_change_completion_models_of_personal_space(space: Space):
    space.user_id = MagicMock()

    with pytest.raises(BadRequestException):
        space.update(completion_models=[MagicMock()])


def test_all_models_are_available_if_personal_space(space: Space):
    space.user_id = MagicMock()

    assert space.completion_models == []

    assert space.is_completion_model_in_space(MagicMock())


def test_permissions_in_personal_space(space: Space):
    user_id = "id"
    user = MagicMock(id=user_id)
    space.user_id = user_id

    assert space.can_read(user)
    assert not space.can_edit(user)
    assert space.can_read_resource(user)
    assert space.can_edit_resource(user)
    assert space.can_delete_resource(user, MagicMock())


def test_can_create_assistants_in_personal_space(space: Space):
    user = MagicMock(permissions={Permission.ASSISTANTS})
    space.user_id = user.id

    assert space.can_create_assistants(user)


def test_can_create_services_in_personal_space(space: Space):
    user = MagicMock(
        permissions={Permission.SERVICES}, modules=[Modules.INTRIC_APPLICATIONS]
    )
    space.user_id = user.id

    assert space.can_create_services(user)


def test_can_not_create_assistants_in_personal_space_without_assistant_permission(
    space: Space,
):
    user = MagicMock()
    space.user_id = user.id

    assert not space.can_create_assistants(user)


def test_can_not_create_services_in_personal_space_without_service_permission(
    space: Space,
):
    user = MagicMock()
    space.user_id = user.id

    assert not space.can_create_services(user)


def test_can_create_assistants_in_shared_space_if_editor_or_admin(space: Space):
    editor = MagicMock(id=1, role=SpaceRole.EDITOR)
    admin = MagicMock(id=2, role=SpaceRole.ADMIN)
    space.members = {1: editor, 2: admin}

    assert space.can_create_assistants(editor)
    assert space.can_create_assistants(admin)


def test_can_create_services_in_shared_space_if_editor_or_admin(space: Space):
    editor = MagicMock(
        id=1, role=SpaceRole.EDITOR, modules=[Modules.INTRIC_APPLICATIONS]
    )
    admin = MagicMock(id=2, role=SpaceRole.ADMIN, modules=[Modules.INTRIC_APPLICATIONS])
    space.members = {1: editor, 2: admin}

    assert space.can_create_services(editor)
    assert space.can_create_services(admin)


def test_can_create_groups_in_personal_space(space: Space):
    user = MagicMock(permissions={Permission.COLLECTIONS})
    space.user_id = user.id

    assert space.can_create_groups(user)


def test_can_not_create_groups_in_personal_space_without_group_permission(
    space: Space,
):
    user = MagicMock()
    space.user_id = user.id

    assert not space.can_create_groups(user)


def test_can_create_groups_in_shared_space_if_editor_or_admin(space: Space):
    editor = MagicMock(id=1, role=SpaceRole.EDITOR)
    admin = MagicMock(id=2, role=SpaceRole.ADMIN)
    space.members = {1: editor, 2: admin}

    assert space.can_create_groups(editor)
    assert space.can_create_groups(admin)


def test_can_create_websites_in_personal_space(space: Space):
    user = MagicMock(permissions={Permission.WEBSITES})
    space.user_id = user.id

    assert space.can_create_websites(user)


def test_can_not_create_websites_in_personal_space_without_website_permission(
    space: Space,
):
    user = MagicMock()
    space.user_id = user.id

    assert not space.can_create_websites(user)


def test_can_create_websites_in_shared_space_if_editor_or_admin(space: Space):
    editor = MagicMock(id=1, role=SpaceRole.EDITOR)
    admin = MagicMock(id=2, role=SpaceRole.ADMIN)
    space.members = {1: editor, 2: admin}

    assert space.can_create_websites(editor)
    assert space.can_create_websites(admin)


def test_can_not_create_websites_if_not_using_intric_proprietary(space: Space):
    SETTINGS.using_intric_proprietary = False
    editor = MagicMock(id=1, role=SpaceRole.EDITOR)
    admin = MagicMock(id=2, role=SpaceRole.ADMIN)
    space.members = {1: editor, 2: admin}

    assert not space.can_create_websites(editor)
    assert not space.can_create_websites(admin)


def test_can_read_members_in_shared_space(space: Space):
    editor = MagicMock(id=1, role=SpaceRole.EDITOR)
    admin = MagicMock(id=2, role=SpaceRole.ADMIN)
    space.members = {1: editor, 2: admin}

    assert space.can_read_members(editor)
    assert space.can_read_members(admin)


def test_no_one_can_read_members_in_personal_space(space: Space):
    editor = MagicMock(id=1, role=SpaceRole.EDITOR)
    admin = MagicMock(id=2, role=SpaceRole.ADMIN)
    space.members = {1: editor, 2: admin}

    space.user_id = MagicMock()

    assert not space.can_read_members(admin)
    assert not space.can_read_members(editor)


async def test_can_create_services_no_intric_applications(space: Space):
    user = MagicMock(modules=[])
    assert not space.can_create_services(user)


async def test_can_create_services_with_intric_applications(space: Space):
    user = MagicMock(id=uuid4(), modules=[Modules.INTRIC_APPLICATIONS])
    space.members = {user.id: user}
    assert space.can_create_services(user)
