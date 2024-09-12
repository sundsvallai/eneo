from uuid import UUID

from pydantic import BaseModel

from instorage.ai_models.completion_models.completion_model import CompletionModelPublic
from instorage.ai_models.embedding_models.embedding_model import EmbeddingModelPublic
from instorage.main.models import InDB


class SettingsBase(BaseModel):
    chatbot_widget: dict = {}


class SettingsUpsert(SettingsBase):
    user_id: UUID


class SettingsInDB(SettingsUpsert, InDB):
    pass


class SettingsPublic(SettingsBase):
    pass


class GetModelsResponse(BaseModel):
    completion_models: list[CompletionModelPublic]
    embedding_models: list[EmbeddingModelPublic]
