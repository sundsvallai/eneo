import os
import pathlib

import yaml

from instorage.ai_models.completion_models.completion_model import (
    CompletionModelCreate,
    CompletionModelUpdate,
)
from instorage.ai_models.completion_models.completion_models_repo import (
    CompletionModelsRepository,
)
from instorage.database.database import sessionmanager
from instorage.main.logging import get_logger

COMPLETION_MODELS_FILE_NAME = "ai_models.yml"

logger = get_logger(__name__)


def load_completion_models_from_config():
    config_path = os.path.join(
        pathlib.Path(__file__).parent.resolve(), COMPLETION_MODELS_FILE_NAME
    )
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
        return data["completion_models"]


async def init_completion_models():
    try:
        completion_models = load_completion_models_from_config()
        async with sessionmanager.session() as session, session.begin():
            repository = CompletionModelsRepository(session=session)

            existing_models = await repository.get_models()
            existing_models_names = {model.name: model.id for model in existing_models}
            new_models_names = [model["name"] for model in completion_models]

            # remove models
            for model in existing_models:
                if model.name not in new_models_names:
                    await repository.delete_model(model.id)

            # create new models or update existing
            for model in completion_models:
                model = CompletionModelCreate(**model)
                if model.name not in existing_models_names:
                    await repository.create_model(model)
                else:
                    model = CompletionModelUpdate(
                        **model.model_dump(), id=existing_models_names[model.name]
                    )
                    await repository.update_model(model)
    except Exception as e:
        logger.error(f"Creating completion models crashed with next error: {str(e)}")
