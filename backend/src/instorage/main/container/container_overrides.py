from dependency_injector import providers

from instorage.ai_models.completion_models.completion_model import CompletionModel
from instorage.ai_models.embedding_models.embedding_model import EmbeddingModel
from instorage.main.container.container import Container
from instorage.users.user import UserInDB


def override_completion_model(container: Container, completion_model: CompletionModel):
    container.config.completion_model.from_value(completion_model.family.value)
    container.completion_model.override(providers.Object(completion_model))

    return container


def override_embedding_model(container: Container, embedding_model: EmbeddingModel):
    container.config.embedding_model.from_value(embedding_model.family.value)
    container.embedding_model.override(providers.Object(embedding_model))

    return container


def override_user(container: Container, user: UserInDB):
    container.user.override(providers.Object(user))
    container.tenant.override(providers.Object(user.tenant))

    return container
