from pydantic import BaseModel, ConfigDict

from instorage.ai_models.completion_models.llms import CompletionModel
from instorage.ai_models.embedding_models.embedding_models import EmbeddingModel
from instorage.main.models import DateTimeModelMixin, IDModelMixin


class SettingsBase(BaseModel):
    chatbot_widget: dict = {}


class SettingsUpsert(SettingsBase):
    user_id: int


class SettingsInDB(SettingsUpsert, IDModelMixin, DateTimeModelMixin):
    model_config = ConfigDict(from_attributes=True)


class SettingsPublic(SettingsBase):
    pass


class GetModelsResponse(BaseModel):
    completion_models: list[CompletionModel]
    embedding_models: list[EmbeddingModel]
