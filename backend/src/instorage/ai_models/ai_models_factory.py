from fastapi import Depends

from instorage.main.container.container import Container
from instorage.server.dependencies.container import get_container


def get_ai_models_service(
    container: Container = Depends(get_container(with_user=True)),
):
    return container.ai_models_service()


def get_embedding_models_repo(container: Container = Depends(get_container())):
    return container.embedding_model_repo()
