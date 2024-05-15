from uuid import UUID

from dependency_injector import providers
from fastapi import Depends

from instorage.ai_models.embedding_models.datastore.datastore import Datastore
from instorage.ai_models.embedding_models.embedding_model_adapters.multilingual_e5_large import (
    MultilingualE5LargeAdapter,
)
from instorage.ai_models.embedding_models.embedding_model_adapters.text_embedding_openai import (
    OpenAIEmbeddingAdapter,
)
from instorage.ai_models.embedding_models.embedding_models import (
    EmbeddingModelName,
    get_embedding_model,
)
from instorage.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from instorage.main.container import Container
from instorage.server.dependencies.container import get_container

MODEL_NAME_TO_ADAPTER_MAP = {
    EmbeddingModelName.TEXT_EMBEDDING_ADA_002: OpenAIEmbeddingAdapter,
    EmbeddingModelName.TEXT_EMBEDDING_3_SMALL: OpenAIEmbeddingAdapter,
    EmbeddingModelName.MULTILINGUAL_E5_LARGE: MultilingualE5LargeAdapter,
}


async def get_datastore(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    group_in_db = await container.group_repo().get_group_by_uuid(id)
    model = get_embedding_model(group_in_db.embedding_model)

    container.config.embedding_model.from_value(model.family.value)
    container.embedding_model.override(providers.Object(model))

    return container.datastore()


def get_datastore_from_model_string(
    model_name: str, info_blob_chunk_repo: InfoBlobChunkRepo
):
    model = get_embedding_model(model_name)
    model_adapter = MODEL_NAME_TO_ADAPTER_MAP[model_name](model)
    return Datastore(
        info_blob_chunk_repo=info_blob_chunk_repo, embedding_model_adapter=model_adapter
    )
