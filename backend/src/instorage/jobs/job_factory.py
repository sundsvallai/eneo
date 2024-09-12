from fastapi import Depends

from instorage.main.container.container import Container
from instorage.server.dependencies.container import get_container


def get_job_service(
    container: Container = Depends(get_container(with_user=True)),
):
    return container.job_service()


def get_task_service(
    container: Container = Depends(get_container(with_user=True)),
):
    return container.task_service()
