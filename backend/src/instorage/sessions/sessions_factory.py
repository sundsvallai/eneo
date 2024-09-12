from fastapi import Depends

from instorage.main.container.container import Container
from instorage.server.dependencies.container import get_container


def get_session_service(container: Container = Depends(get_container(with_user=True))):
    return container.session_service()


def get_session_service_from_assistant_api_key(
    container: Container = Depends(
        get_container(with_user_from_assistant_api_key=True)
    ),
):
    return container.session_service()
