from typing import Annotated

from fastapi import Header, WebSocketException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader

from intric.main.config import get_settings

_login_endpoint = f"{get_settings().api_prefix}/users/login/token/"
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=_login_endpoint, auto_error=False)
API_KEY_HEADER = APIKeyHeader(name=get_settings().api_key_header_name, auto_error=False)

AUTH_PREFIX = "auth_"


async def get_token_from_websocket_header(
    sec_websocket_protocol: Annotated[str | None, Header()] = None
):
    if sec_websocket_protocol is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    for header in sec_websocket_protocol.split(', '):
        if header.startswith(AUTH_PREFIX):
            return header[len(AUTH_PREFIX) :]

    # If there is no Bearer token in the header, raise
    raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
