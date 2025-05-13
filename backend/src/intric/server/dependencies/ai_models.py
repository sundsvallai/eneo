import os
import pathlib

import yaml

from intric.ai_models.completion_models.completion_model import (
    CompletionModelCreate,
    CompletionModelUpdate,
)
from intric.ai_models.completion_models.completion_models_repo import (
    CompletionModelsRepository,
)
from intric.ai_models.embedding_models.embedding_model import (
    EmbeddingModelCreate,
    EmbeddingModelUpdate,
)
from intric.ai_models.embedding_models.embedding_models_repo import (
    AdminEmbeddingModelsService,
)
from intric.database.database import sessionmanager
from intric.main.logging import get_logger

COMPLETION_MODELS_FILE_NAME = "ai_models.yml"

logger = get_logger(__name__)


def load_models_from_config():
    config_path = os.path.join(pathlib.Path(__file__).parent.resolve(), COMPLETION_MODELS_FILE_NAME)
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
        return data


async def create_models(
    models: dict,
    repository: type[CompletionModelsRepository] | type[AdminEmbeddingModelsService],
    model_create: type[CompletionModelCreate] | type[EmbeddingModelCreate],
    model_update: type[CompletionModelUpdate] | type[EmbeddingModelUpdate],
):
    async with sessionmanager.session() as session, session.begin():
        repository = repository(session=session)

        existing_models = await repository.get_ids_and_names()
        existing_models_names = {model.name: model.id for model in existing_models}
        new_models_names = [model["name"] for model in models]

        # remove models
        for model in existing_models:
            if model.name not in new_models_names:
                await repository.delete_model(model.id)

        # create new models or update existing
        for model in models:
            model = model_create(**model)
            if model.name not in existing_models_names:
                await repository.create_model(model)
            else:
                model = model_update(**model.model_dump(), id=existing_models_names[model.name])
                await repository.update_model(model)


async def init_models():
    try:
        data = load_models_from_config()

        logger.info("Completion Models initialization...")
        completion_models = data["completion_models"]
        await create_models(
            models=completion_models,
            repository=CompletionModelsRepository,
            model_create=CompletionModelCreate,
            model_update=CompletionModelUpdate,
        )
        logger.info("Completion Models initialization completed.")

        logger.info("Embedding Models initialization...")
        embedding_models = data["embedding_models"]
        await create_models(
            models=embedding_models,
            repository=AdminEmbeddingModelsService,
            model_create=EmbeddingModelCreate,
            model_update=EmbeddingModelUpdate,
        )
        logger.info("Embedding Models initialization completed.")

    except Exception as e:
        logger.exception(f"Creating models crashed with next error: {str(e)}")
