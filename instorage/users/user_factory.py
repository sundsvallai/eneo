from fastapi import Depends

from instorage.main.container import Container
from instorage.server.dependencies.container import get_container


def get_user_service(container: Container = Depends(get_container())):
    return container.user_service()
