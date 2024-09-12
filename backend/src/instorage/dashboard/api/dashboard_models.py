from pydantic import BaseModel

from instorage.main.models import PaginatedResponse
from instorage.spaces.api.space_models import SpaceDashboard


class Dashboard(BaseModel):
    spaces: PaginatedResponse[SpaceDashboard]
