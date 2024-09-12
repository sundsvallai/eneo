from fastapi import Depends

from instorage.main.container.container import Container
from instorage.server.dependencies.container import get_container


def get_groups_service(container: Container = Depends(get_container(with_user=True))):
    return container.group_service()


def get_groups_service_from_assistant_api_key(
    container: Container = Depends(
        get_container(with_user_from_assistant_api_key=True)
    ),
):
    return container.group_service()
