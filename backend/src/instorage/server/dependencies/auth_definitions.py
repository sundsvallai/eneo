from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader

from instorage.main.config import get_settings

_login_endpoint = f"{get_settings().api_prefix}/users/login/token/"
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=_login_endpoint, auto_error=False)
API_KEY_HEADER = APIKeyHeader(name=get_settings().api_key_header_name, auto_error=False)
