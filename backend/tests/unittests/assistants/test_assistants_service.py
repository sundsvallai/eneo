from copy import deepcopy
from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from instorage.ai_models.ai_models_service import AIModelsService
from instorage.assistants.api.assistant_models import (
    AskAssistant,
    AssistantBase,
    AssistantCreatePublic,
    AssistantUpdatePublic,
)
from instorage.assistants.assistant_factory import AssistantFactory
from instorage.assistants.assistant_service import AssistantService
from instorage.main.config import get_settings
from instorage.main.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from instorage.main.models import ModelId
from tests.fixtures import (
    TEST_ASSISTANT,
    TEST_GROUP,
    TEST_MODEL_GPT4,
    TEST_USER,
    TEST_UUID,
)


@dataclass
class Setup:
    assistant: AssistantBase
    service: AssistantService
    group_service: AsyncMock


@pytest.fixture(name="setup")
def setup_fixture():
    repo = AsyncMock()
    user = TEST_USER
    auth_service = MagicMock()
    assistant = AssistantCreatePublic(
        name="test_name",
        prompt="test_prompt",
        completion_model=ModelId(id=TEST_MODEL_GPT4.id),
    )

    ai_models_service = AIModelsService(
        user=TEST_USER,
        embedding_model_repo=AsyncMock(),
        completion_model_repo=AsyncMock(),
        tenant_repo=AsyncMock(),
    )

    service = AssistantService(
        repo,
        user,
        auth_service,
        AsyncMock(),
        AsyncMock(),
        ai_models_service=ai_models_service,
        group_service=AsyncMock(),
        website_service=AsyncMock(),
        space_service=AsyncMock(),
        factory=AssistantFactory(),
    )

    setup = Setup(assistant=assistant, service=service, group_service=AsyncMock())

    return setup


def with_two_different_groups(setup: Setup, attr: str, value_1: Any, value_2: Any):
    group_1 = deepcopy(TEST_GROUP)
    group_2 = deepcopy(TEST_GROUP)

    setattr(group_1, attr, value_1)
    setattr(group_2, attr, value_2)

    assistant = deepcopy(TEST_ASSISTANT)
    assistant.groups = [group_1, group_2]

    setup.service.repo.add.return_value = assistant
    setup.service.repo.update.return_value = assistant
    setup.service.user.id = 1
    setup.service.user.tenant_id = 1


async def test_create_assistant_with_logging_fails_without_compliance_permission(
    setup: Setup,
):
    setup.service.user = MagicMock()
    setup.service.user.permissions = {}
    setup.assistant.logging_enabled = True
    with pytest.raises(UnauthorizedException):
        await setup.service.create_assistant(setup.assistant)


async def test_create_public_assistant_fails_when_not_deployer(setup: Setup):
    setup.service.user = MagicMock()
    setup.service.user.permissions = {}
    with pytest.raises(UnauthorizedException):
        await setup.service.create_assistant(setup.assistant)


async def test_get_assistant_fails_when_not_owner(setup: Setup):
    user = MagicMock(id=uuid4())
    setup.service.user = MagicMock(id=uuid4())
    setup.service.user = user
    setup.service.repo.get_by_id.return_value = TEST_ASSISTANT

    with pytest.raises(NotFoundException):
        await setup.service.get_assistant(TEST_ASSISTANT.id)


async def test_ask_assistant_model():
    files_number = get_settings().max_in_question + 1
    files = [ModelId(id=uuid4()) for _ in range(files_number)]

    with pytest.raises(ValidationError):
        AskAssistant(question="test", files=files)


async def test_update_space_assistant_not_member(setup: Setup):
    assistant_update = AssistantUpdatePublic(prompt="new prompt!")

    space = MagicMock()
    space.can_edit_resource.return_value = False
    setup.service.space_service.get_space.return_value = space

    with pytest.raises(UnauthorizedException):
        await setup.service.update_assistant(assistant_update, TEST_UUID)


async def test_update_space_assistant_member(setup: Setup):
    assistant_update = AssistantUpdatePublic(prompt="new prompt!")

    space = MagicMock()
    space.can_edit_resource.return_value = True
    setup.service.space_service.get_space.return_value = space

    await setup.service.update_assistant(assistant_update, TEST_UUID)


async def test_delete_space_assistant_not_member(setup: Setup):
    space = MagicMock()
    space.can_delete_resource.return_value = False
    setup.service.space_service.get_space.return_value = space

    with pytest.raises(UnauthorizedException):
        await setup.service.delete_assistant(TEST_UUID)


async def test_delete_space_assistant_member(setup: Setup):
    space = MagicMock()
    space.can_delete_resource.return_value = True
    setup.service.space_service.get_space.return_value = space

    await setup.service.delete_assistant(TEST_UUID)


async def test_update_assistant_completion_model_not_in_space(setup: Setup):
    space = MagicMock()
    space.is_completion_model_in_space.return_value = False
    setup.service.space_service.get_space.return_value = space

    with pytest.raises(
        BadRequestException,
        match="Completion model is not in space.",
    ):
        await setup.service.update_assistant(TEST_UUID)


async def test_update_assistant_completion_model_in_space(setup: Setup):
    space = MagicMock()
    space.is_completion_model_in_space.return_value = True
    setup.service.space_service.get_space.return_value = space

    await setup.service.update_assistant(TEST_UUID)


async def test_update_assistant_group_not_in_space(setup: Setup):
    space = MagicMock()
    space.is_group_in_space.return_value = False
    setup.service.space_service.get_space.return_value = space

    assistant = MagicMock(groups=[MagicMock()])
    setup.service.repo.update.return_value = assistant

    with pytest.raises(
        BadRequestException,
        match="Group is not in space.",
    ):
        await setup.service.update_assistant(id=TEST_UUID, prompt="new prompt!")


async def test_update_assistant_group_in_space(setup: Setup):
    space = MagicMock()
    space.is_group_in_space.return_value = True
    setup.service.space_service.get_space.return_value = space

    assistant = MagicMock(groups=[MagicMock()])
    setup.service.repo.update.return_value = assistant

    await setup.service.update_assistant(TEST_UUID)


async def test_update_assistant_website_not_in_space(setup: Setup):
    space = MagicMock()
    space.is_website_in_space.return_value = False
    setup.service.space_service.get_space.return_value = space

    assistant = MagicMock(websites=[MagicMock()])
    setup.service.repo.update.return_value = assistant

    with pytest.raises(
        BadRequestException,
        match="Website is not in space.",
    ):
        await setup.service.update_assistant(TEST_UUID)


async def test_update_assistant_website_in_space(setup: Setup):
    space = MagicMock()
    space.is_website_in_space.return_value = True
    setup.service.space_service.get_space.return_value = space

    assistant = MagicMock(websites=[MagicMock()])
    setup.service.repo.update.return_value = assistant

    await setup.service.update_assistant(TEST_UUID)
