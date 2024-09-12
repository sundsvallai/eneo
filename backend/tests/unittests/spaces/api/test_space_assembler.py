from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from instorage.ai_models.completion_models.completion_model import (
    CompletionModelFamily,
    CompletionModelSparse,
    ModelHostingLocation,
    ModelStability,
)
from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModelFamily,
    EmbeddingModelSparse,
)
from instorage.assistants.api.assistant_models import AssistantSparse
from instorage.groups.group import GroupMetadata, GroupSparse
from instorage.main.models import IdAndName, PaginatedPermissions, ResourcePermissions
from instorage.services.service import ServiceSparse
from instorage.spaces.api.space_assembler import SpaceAssembler
from instorage.spaces.api.space_models import (
    Applications,
    Knowledge,
    SpaceMember,
    SpacePublic,
    SpaceRole,
)
from instorage.spaces.space import Space
from instorage.websites.website_models import WebsiteSparse
from tests.fixtures import TEST_UUID

TEST_NAME = "test_name"
TEST_ASSISTANT = AssistantSparse(
    id=TEST_UUID, name=TEST_NAME, is_published=False, prompt="", user_id=TEST_UUID
)
TEST_SERVICE = ServiceSparse(id=TEST_UUID, name=TEST_NAME, prompt="", user_id=TEST_UUID)
TEST_GROUP = GroupSparse(
    id=TEST_UUID,
    name=TEST_NAME,
    metadata=GroupMetadata(num_info_blobs=10),
    user_id=TEST_UUID,
    embedding_model=IdAndName(id=TEST_UUID, name=TEST_NAME),
)
TEST_WEBSITE = WebsiteSparse(
    id=TEST_UUID,
    name=TEST_NAME,
    url="www.example.com",
    user_id=TEST_UUID,
    embedding_model=IdAndName(id=TEST_UUID, name=TEST_NAME),
)


@pytest.fixture
def space_assembler():
    return SpaceAssembler(MagicMock())


@pytest.fixture
def space():
    space = MagicMock(
        id=TEST_UUID,
        user_id=None,
        tenant_id=TEST_UUID,
        description=None,
        embedding_models=[],
        completion_models=[],
        assistants=[],
        services=[],
        websites=[],
        groups=[],
        members={},
    )
    space.name = TEST_NAME

    return space


def test_from_space_to_model(space_assembler: SpaceAssembler):
    test_name = "test_name"
    now = datetime.now()

    embedding_model = EmbeddingModelSparse(
        id=TEST_UUID,
        name=test_name,
        family=EmbeddingModelFamily.E5,
        is_deprecated=False,
        open_source=True,
        stability=ModelStability.EXPERIMENTAL,
        hosting=ModelHostingLocation.EU,
    )
    completion_model = CompletionModelSparse(
        id=TEST_UUID,
        name=test_name,
        nickname=test_name,
        family=CompletionModelFamily.AZURE,
        token_limit=100,
        is_deprecated=False,
        stability=ModelStability.STABLE,
        hosting=ModelHostingLocation.USA,
        vision=True,
    )
    assistant = AssistantSparse(
        id=TEST_UUID,
        name=test_name,
        is_published=False,
        prompt="",
        user_id=TEST_UUID,
        permissions=[ResourcePermissions.EDIT, ResourcePermissions.DELETE],
    )
    service = ServiceSparse(
        id=TEST_UUID,
        name=test_name,
        prompt="",
        user_id=TEST_UUID,
        permissions=[ResourcePermissions.EDIT, ResourcePermissions.DELETE],
    )
    tenant_id = TEST_UUID
    admin = SpaceMember(
        id=TEST_UUID,
        email="admin@example.com",
        username="admin",
        role=SpaceRole.ADMIN,
        created_at=now,
    )
    editor = SpaceMember(
        id=uuid4(),
        email="editor@example.com",
        username="editor",
        role=SpaceRole.EDITOR,
        created_at=now + timedelta(seconds=1),
    )

    expected_space = SpacePublic(
        created_at=now,
        updated_at=now,
        id=TEST_UUID,
        name=test_name,
        description=None,
        personal=False,
        embedding_models=[embedding_model],
        completion_models=[completion_model],
        applications=Applications(
            assistants=PaginatedPermissions[AssistantSparse](
                permissions=[ResourcePermissions.READ, ResourcePermissions.CREATE],
                items=[assistant],
            ),
            services=PaginatedPermissions[ServiceSparse](
                permissions=[ResourcePermissions.READ, ResourcePermissions.CREATE],
                items=[service],
            ),
        ),
        knowledge=Knowledge(
            groups=PaginatedPermissions[GroupSparse](
                permissions=[ResourcePermissions.READ, ResourcePermissions.CREATE],
                items=[TEST_GROUP],
            ),
            websites=PaginatedPermissions[WebsiteSparse](
                permissions=[ResourcePermissions.READ, ResourcePermissions.CREATE],
                items=[TEST_WEBSITE],
            ),
        ),
        members=PaginatedPermissions[SpaceMember](
            permissions=[
                ResourcePermissions.READ,
                ResourcePermissions.ADD,
                ResourcePermissions.EDIT,
                ResourcePermissions.REMOVE,
            ],
            items=[admin, editor],
        ),
        permissions=[
            ResourcePermissions.READ,
            ResourcePermissions.EDIT,
            ResourcePermissions.DELETE,
        ],
    )

    space = MagicMock(
        created_at=now,
        updated_at=now,
        id=TEST_UUID,
        user_id=None,
        description=None,
        embedding_models=[embedding_model],
        completion_models=[completion_model],
        assistants=[assistant],
        services=[service],
        websites=[TEST_WEBSITE],
        groups=[TEST_GROUP],
        tenant_id=tenant_id,
        members={admin.id: admin, editor.id: editor},
    )
    space.name = test_name

    space_assembler.user = MagicMock(id=admin.id)
    space_public = space_assembler.from_space_to_model(space)

    assert space_public == expected_space


def test_from_personal_space_to_model_sets_personal(
    space: Space, space_assembler: SpaceAssembler
):
    space.user_id = TEST_UUID

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.personal


def test_set_permissions_on_assistants(space: Space, space_assembler: SpaceAssembler):
    space.can_create_assistants.return_value = True

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.applications.assistants.permissions == [
        ResourcePermissions.READ,
        ResourcePermissions.CREATE,
    ]


def test_set_permissions_on_services(space: Space, space_assembler: SpaceAssembler):
    space.can_create_services.return_value = True

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.applications.services.permissions == [
        ResourcePermissions.READ,
        ResourcePermissions.CREATE,
    ]


def test_set_permissions_on_assistant_without_permission(
    space: Space, space_assembler: SpaceAssembler
):
    space.can_create_assistants.return_value = False

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.applications.assistants.permissions == []


def test_set_permissions_on_services_without_permission(
    space: Space, space_assembler: SpaceAssembler
):
    space.can_create_services.return_value = False

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.applications.services.permissions == []


def test_set_permissions_on_groups(space: Space, space_assembler: SpaceAssembler):
    space.can_create_groups.return_value = True

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.knowledge.groups.permissions == [
        ResourcePermissions.READ,
        ResourcePermissions.CREATE,
    ]


def test_set_permissions_on_groups_without_permission(
    space: Space, space_assembler: SpaceAssembler
):
    space.can_create_groups.return_value = False

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.knowledge.groups.permissions == []


def test_set_permissions_on_websites(space: Space, space_assembler: SpaceAssembler):
    space.can_create_websites.return_value = True

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.knowledge.websites.permissions == [
        ResourcePermissions.READ,
        ResourcePermissions.CREATE,
    ]


def test_set_permissions_on_websites_without_permission(
    space: Space, space_assembler: SpaceAssembler
):
    space.can_create_websites.return_value = False

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.knowledge.websites.permissions == []


@pytest.mark.parametrize(
    [
        "can_read",
        "can_edit",
        "expected_permissions",
    ],
    [
        [False, False, []],
        [True, False, [ResourcePermissions.READ]],
        [False, True, [ResourcePermissions.EDIT, ResourcePermissions.DELETE]],
        [
            True,
            True,
            [
                ResourcePermissions.READ,
                ResourcePermissions.EDIT,
                ResourcePermissions.DELETE,
            ],
        ],
    ],
)
def test_set_space_permissions(
    space: Space,
    space_assembler: SpaceAssembler,
    can_read: bool,
    can_edit: bool,
    expected_permissions: list[ResourcePermissions],
):
    space.can_read.return_value = can_read
    space.can_edit.return_value = can_edit

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.permissions == expected_permissions


@pytest.mark.parametrize(
    [
        "can_read_members",
        "can_edit",
        "expected_permissions",
    ],
    [
        [False, False, []],
        [True, False, [ResourcePermissions.READ]],
        [
            False,
            True,
            [
                ResourcePermissions.ADD,
                ResourcePermissions.EDIT,
                ResourcePermissions.REMOVE,
            ],
        ],
        [
            True,
            True,
            [
                ResourcePermissions.READ,
                ResourcePermissions.ADD,
                ResourcePermissions.EDIT,
                ResourcePermissions.REMOVE,
            ],
        ],
    ],
)
def test_set_members_permissions(
    space: Space,
    space_assembler: SpaceAssembler,
    can_read_members: bool,
    can_edit: bool,
    expected_permissions: list[ResourcePermissions],
):
    space.can_read_members.return_value = can_read_members
    space.can_edit.return_value = can_edit
    space_public = space_assembler.from_space_to_model(space)

    assert space_public.members.permissions == expected_permissions


@pytest.mark.parametrize(
    [
        "can_read_resource",
        "can_edit_resource",
        "can_delete_resource",
        "expected_permissions",
    ],
    [
        [False, False, False, []],
        [True, False, False, [ResourcePermissions.READ]],
        [False, True, False, [ResourcePermissions.EDIT]],
        [False, False, True, [ResourcePermissions.DELETE]],
        [True, True, False, [ResourcePermissions.READ, ResourcePermissions.EDIT]],
        [True, False, True, [ResourcePermissions.READ, ResourcePermissions.DELETE]],
        [False, True, True, [ResourcePermissions.EDIT, ResourcePermissions.DELETE]],
        [
            True,
            True,
            True,
            [
                ResourcePermissions.READ,
                ResourcePermissions.EDIT,
                ResourcePermissions.DELETE,
            ],
        ],
    ],
)
def test_set_resource_permissions_on_assistants(
    space: Space,
    space_assembler: SpaceAssembler,
    can_read_resource: bool,
    can_edit_resource: bool,
    can_delete_resource: bool,
    expected_permissions: list[ResourcePermissions],
):
    space.can_read_resource.return_value = can_read_resource
    space.can_edit_resource.return_value = can_edit_resource
    space.can_delete_resource.return_value = can_delete_resource

    space.assistants = [TEST_ASSISTANT]

    space_public = space_assembler.from_space_to_model(space)

    assert (
        space_public.applications.assistants.items[0].permissions
        == expected_permissions
    )


@pytest.mark.parametrize(
    [
        "can_read_resource",
        "can_edit_resource",
        "can_delete_resource",
        "expected_permissions",
    ],
    [
        [False, False, False, []],
        [True, False, False, [ResourcePermissions.READ]],
        [False, True, False, [ResourcePermissions.EDIT]],
        [False, False, True, [ResourcePermissions.DELETE]],
        [True, True, False, [ResourcePermissions.READ, ResourcePermissions.EDIT]],
        [True, False, True, [ResourcePermissions.READ, ResourcePermissions.DELETE]],
        [False, True, True, [ResourcePermissions.EDIT, ResourcePermissions.DELETE]],
        [
            True,
            True,
            True,
            [
                ResourcePermissions.READ,
                ResourcePermissions.EDIT,
                ResourcePermissions.DELETE,
            ],
        ],
    ],
)
def test_set_resource_permissions_on_services(
    space: Space,
    space_assembler: SpaceAssembler,
    can_read_resource: bool,
    can_edit_resource: bool,
    can_delete_resource: bool,
    expected_permissions: list[ResourcePermissions],
):
    space.can_read_resource.return_value = can_read_resource
    space.can_edit_resource.return_value = can_edit_resource
    space.can_delete_resource.return_value = can_delete_resource

    space.services = [TEST_SERVICE]

    space_public = space_assembler.from_space_to_model(space)

    assert (
        space_public.applications.services.items[0].permissions == expected_permissions
    )


@pytest.mark.parametrize(
    [
        "can_read_resource",
        "can_edit_resource",
        "can_delete_resource",
        "expected_permissions",
    ],
    [
        [False, False, False, []],
        [True, False, False, [ResourcePermissions.READ]],
        [False, True, False, [ResourcePermissions.EDIT]],
        [False, False, True, [ResourcePermissions.DELETE]],
        [True, True, False, [ResourcePermissions.READ, ResourcePermissions.EDIT]],
        [True, False, True, [ResourcePermissions.READ, ResourcePermissions.DELETE]],
        [False, True, True, [ResourcePermissions.EDIT, ResourcePermissions.DELETE]],
        [
            True,
            True,
            True,
            [
                ResourcePermissions.READ,
                ResourcePermissions.EDIT,
                ResourcePermissions.DELETE,
            ],
        ],
    ],
)
def test_set_resource_permissions_on_groups(
    space: Space,
    space_assembler: SpaceAssembler,
    can_read_resource: bool,
    can_edit_resource: bool,
    can_delete_resource: bool,
    expected_permissions: list[ResourcePermissions],
):
    space.can_read_resource.return_value = can_read_resource
    space.can_edit_resource.return_value = can_edit_resource
    space.can_delete_resource.return_value = can_delete_resource

    space.groups = [TEST_GROUP]

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.knowledge.groups.items[0].permissions == expected_permissions


@pytest.mark.parametrize(
    [
        "can_read_resource",
        "can_edit_resource",
        "can_delete_resource",
        "expected_permissions",
    ],
    [
        [False, False, False, []],
        [True, False, False, [ResourcePermissions.READ]],
        [False, True, False, [ResourcePermissions.EDIT]],
        [False, False, True, [ResourcePermissions.DELETE]],
        [True, True, False, [ResourcePermissions.READ, ResourcePermissions.EDIT]],
        [True, False, True, [ResourcePermissions.READ, ResourcePermissions.DELETE]],
        [False, True, True, [ResourcePermissions.EDIT, ResourcePermissions.DELETE]],
        [
            True,
            True,
            True,
            [
                ResourcePermissions.READ,
                ResourcePermissions.EDIT,
                ResourcePermissions.DELETE,
            ],
        ],
    ],
)
def test_set_resource_permissions_on_websites(
    space: Space,
    space_assembler: SpaceAssembler,
    can_read_resource: bool,
    can_edit_resource: bool,
    can_delete_resource: bool,
    expected_permissions: list[ResourcePermissions],
):
    space.can_read_resource.return_value = can_read_resource
    space.can_edit_resource.return_value = can_edit_resource
    space.can_delete_resource.return_value = can_delete_resource

    space.websites = [TEST_WEBSITE]

    space_public = space_assembler.from_space_to_model(space)

    assert space_public.knowledge.websites.items[0].permissions == expected_permissions


def test_space_members_ordering(space: Space, space_assembler: SpaceAssembler):
    admin = SpaceMember(
        id=TEST_UUID,
        email="admin@example.com",
        username="admin",
        role=SpaceRole.ADMIN,
    )
    editor = SpaceMember(
        id=uuid4(),
        email="editor@example.com",
        username="editor",
        role=SpaceRole.EDITOR,
    )
    editor_2 = SpaceMember(
        id=uuid4(),
        email="editor2@example.com",
        username="editor2",
        role=SpaceRole.EDITOR,
    )

    space.members = {admin.id: admin, editor.id: editor, editor_2.id: editor_2}

    space_assembler.user = MagicMock(id=editor_2.id)
    space_public = space_assembler.from_space_to_model(space)

    assert space_public.members.items == [editor_2, admin, editor]
