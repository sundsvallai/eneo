from contextlib import asynccontextmanager
from typing import Callable
from uuid import UUID

from dependency_injector import providers

from instorage.ai_models.embedding_models.embedding_models import get_embedding_model
from instorage.database.database import sessionmanager
from instorage.jobs.task_models import UploadTask
from instorage.main.container import Container


@asynccontextmanager
async def get_container(user_id: UUID, group_id: UUID):
    async with sessionmanager.session() as session:
        container = Container(
            session=providers.Object(session),
        )

        async with session.begin():
            user_in_db = await container.user_repo().get_user_by_uuid(user_id)
            group_in_db = await container.group_repo().get_group_by_uuid(group_id)
            embedding_model = get_embedding_model(group_in_db.embedding_model)

        container.config.embedding_model.from_value(embedding_model.family.value)
        container.embedding_model.override(providers.Object(embedding_model))
        container.user.override(providers.Object(user_in_db))
        container.tenant.override(providers.Object(user_in_db.tenant))

        yield container


@asynccontextmanager
async def get_task_manager(job_id: UUID, container: Container):
    task_manager = container.task_manager(job_id=job_id)

    async with task_manager.set_status_on_exception():
        yield task_manager


def task(func: Callable):
    """Functions decorated with this decorator should:

    Take three keyword-only arguments as input, params, container, and task_manager.
    Output a string, which is the result location where the resources can be found.
    """

    async def _task(*, job_id: UUID, params: UploadTask):
        async with get_container(
            user_id=params.user_id, group_id=params.group_id
        ) as container:
            async with get_task_manager(
                job_id=job_id, container=container
            ) as task_manager:
                result_location = await func(
                    params=params, container=container, task_manager=task_manager
                )
                task_manager.result_location = result_location

        return task_manager.successful()

    return _task
