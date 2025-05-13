from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from intric.spaces.space_factory import SpaceFactory


@pytest.fixture
def factory():
    return SpaceFactory(MagicMock(), MagicMock())


def test_create_space_from_request():
    name = "test space"
    created_space = SpaceFactory.create_space(name=name, tenant_id=uuid4())

    assert created_space.id is None
    assert created_space.name == name
    assert created_space.description is None
    assert created_space.embedding_models == []
    assert created_space.completion_models == []
    assert created_space.tenant_id is not None
    assert created_space.members == {}
