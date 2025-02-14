from pydantic import BaseModel

from intric.main.models import PaginatedResponse
from intric.spaces.api.space_models import SpaceDashboard


class Dashboard(BaseModel):
    spaces: PaginatedResponse[SpaceDashboard]
