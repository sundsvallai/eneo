# Copyright (c) 2023 Sundsvalls Kommun
#
# Licensed under the MIT License.

from typing import Optional

from pydantic import BaseModel, ConfigDict, Json

from instorage.main.models import InDB


class LoggingDetails(BaseModel):
    context: Optional[str] = None
    model_kwargs: dict
    json_body: Optional[str] = None

    model_config = ConfigDict(protected_namespaces=())


class LoggingDetailsInDB(LoggingDetails, InDB):
    pass


class LoggingDetailsPublic(LoggingDetails):
    json_body: Json
