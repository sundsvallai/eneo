from typing import Optional

from pydantic import BaseModel, HttpUrl


class PrivacyPolicy(BaseModel):
    url: Optional[HttpUrl] = None
