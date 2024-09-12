from uuid import UUID

from dependency_injector import providers
from fastapi import Depends

from instorage.ai_models.embedding_models.datastore.datastore import Datastore
from instorage.ai_models.embedding_models.embedding_model import EmbeddingModelFamily
from instorage.ai_models.embedding_models.embedding_model_adapters.infinity_adapter import (
    InfinityAdapter,
)
from instorage.ai_models.embedding_models.embedding_model_adapters.text_embedding_openai import (
    OpenAIEmbeddingAdapter,
)
from instorage.ai_models.embedding_models.embedding_models_repo import (
    EmbeddingModelsRepository,
)
from instorage.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from instorage.main.container.container import Container
from instorage.server.dependencies.container import get_container


async def get_datastore(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    group_in_db = await container.group_repo().get_group(id)
    model = group_in_db.embedding_model

    container.config.embedding_model.from_value(model.family.value)
    container.embedding_model.override(providers.Object(model))

    return container.datastore()


async def get_datastore_from_model_id(
    model_id: UUID,
    info_blob_chunk_repo: InfoBlobChunkRepo,
    embedding_model_repo: EmbeddingModelsRepository,
):
    model = await embedding_model_repo.get_model(model_id)

    if model.family == EmbeddingModelFamily.OPEN_AI:
        model_adapter = OpenAIEmbeddingAdapter(model=model)
    else:
        model_adapter = InfinityAdapter(model=model)

    return Datastore(
        info_blob_chunk_repo=info_blob_chunk_repo, embedding_model_adapter=model_adapter
    )
