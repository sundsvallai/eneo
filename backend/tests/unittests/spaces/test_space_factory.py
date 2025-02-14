from unittest.mock import MagicMock

import pytest

from intric.spaces.space_factory import SpaceFactory
from tests.fixtures import TEST_UUID


@pytest.fixture
def factory():
    return SpaceFactory()


def test_create_space_from_request():
    name = "test space"
    created_space = SpaceFactory.create_space(name=name)

    assert created_space.id is None
    assert created_space.name == name
    assert created_space.description is None
    assert created_space.embedding_models == []
    assert created_space.completion_models == []
    assert created_space.tenant_id is None
    assert created_space.members == {}


def test_create_space_with_assistants_and_default_assistant(factory: SpaceFactory):
    # Setup
    normal_assistant = MagicMock(
        id=TEST_UUID,
        completion_model_kwargs={},
        user_id=TEST_UUID,
        is_default=False,
    )
    normal_assistant.name = "normal assistant"
    default_assistant = MagicMock(
        id=TEST_UUID, completion_model_kwargs={}, user_id=TEST_UUID, is_default=True
    )
    default_assistant.name = "default assistant"
    space_in_db = MagicMock()

    # Run
    space = factory.create_space_from_db(
        space_in_db=space_in_db,
        user=MagicMock(),
        default_assistant=default_assistant,
        assistants=[normal_assistant, default_assistant],
    )

    # Assert
    assert space.assistants == [normal_assistant]
    assert space.default_assistant == default_assistant
