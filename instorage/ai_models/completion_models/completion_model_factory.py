from fastapi import Depends

from instorage.main.container import Container
from instorage.server.dependencies.container import get_container


def get_completion_models_service(
    container: Container = Depends(get_container(with_user=True)),
):
    return container.completion_model_service()
