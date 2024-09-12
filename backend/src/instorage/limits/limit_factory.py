from fastapi import Depends

from instorage.main.container.container import Container
from instorage.server.dependencies.container import get_container


def get_limit_service(container: Container = Depends(get_container())):
    return container.limit_service()
