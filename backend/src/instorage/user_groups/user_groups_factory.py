# MIT License

from fastapi import Depends

from instorage.main.container.container import Container
from instorage.server.dependencies.container import get_container


def get_user_groups_service(
    container: Container = Depends(get_container(with_user=True)),
):
    return container.user_group_service()
