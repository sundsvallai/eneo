# MIT License

from typing import Optional

from pydantic import BaseModel, ConfigDict, Json


class LoggingDetails(BaseModel):
    context: Optional[str] = None
    model_kwargs: dict
    json_body: Optional[str] = None

    model_config = ConfigDict(protected_namespaces=())


class LoggingDetailsInDB(LoggingDetails):
    id: int

    model_config = ConfigDict(from_attributes=True)


class LoggingDetailsPublic(LoggingDetails):
    json_body: Json
