from fastapi import Depends

from instorage.main.container import Container
from instorage.server.dependencies.container import get_container


def get_admin_service(container: Container = Depends(get_container(with_user=True))):
    return container.admin_service()
