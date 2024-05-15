from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from instorage.main.config import get_jwt_audience, get_jwt_expiry_time_minutes

JWT_AUDIENCE = get_jwt_audience()
JWT_EXPIRY_TIME_MINUTES = get_jwt_expiry_time_minutes()


class OIDCProviders(str, Enum):
    MOBILITY_GUARD = "mobility_guard"


class JWTMeta(BaseModel):
    iss: str = "inoolabs.com"  # who issued it
    aud: str = JWT_AUDIENCE  # who it's intended for
    iat: float = datetime.timestamp(datetime.utcnow())  # issued at time
    exp: float = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=JWT_EXPIRY_TIME_MINUTES)
    )  # expiry time


class JWTCreds(BaseModel):
    """How we'll identify users"""

    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """

    pass


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class ApiKeyPublic(BaseModel):
    truncated_key: str


class ApiKey(ApiKeyPublic):
    key: str


class ApiKeyCreated(ApiKey):
    hashed_key: str


class ApiKeyInDB(ApiKey):
    user_id: Optional[int]
    assistant_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class CreateUserResponse(BaseModel):
    token: AccessToken
    api_key: ApiKey


class OpenIdConnectLogin(BaseModel):
    code: str
    code_verifier: str
    redirect_uri: str
    client_id: str = "intric"
    grant_type: str = "authorization_code"
    scope: str = "openid"
    nonce: str = None
