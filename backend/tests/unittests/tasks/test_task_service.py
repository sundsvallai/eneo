from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from instorage.groups.group_service import GroupService
from instorage.jobs.task_service import TaskService
from instorage.main.exceptions import BadRequestException


@pytest.fixture
def service():
    group_service = GroupService(
        user=MagicMock(),
        repo=AsyncMock(),
        tenant_repo=AsyncMock(),
        info_blob_repo=AsyncMock(),
        ai_models_service=AsyncMock(),
        space_service=AsyncMock(),
    )
    return TaskService(
        user=MagicMock(),
        group_service=group_service,
        file_size_service=AsyncMock(),
        job_service=AsyncMock(),
    )


async def test_space_group_embedding_model_not_in_space(service: TaskService):
    space = MagicMock()
    space.is_embedding_model_in_space.return_value = False
    service.group_service.space_service.get_space.return_value = space

    with pytest.raises(BadRequestException):
        await service.queue_upload_file(
            group_id=uuid4(),
            file=MagicMock(),
            mimetype="application/pdf",
            filename="test",
        )
