from fastapi import Security
from intric.main.exceptions import AuthenticationException
from intric.main.logging import get_logger
from intric.server.dependencies.auth_definitions import API_KEY_HEADER
from intric.main.config import get_settings

logger = get_logger(__name__)


def authenticate_super_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    super_api_key = get_settings().intric_super_api_key

    if super_api_key == api_key_header:
        return api_key_header
    else:
        raise AuthenticationException("Unauthorized")


def authenticate_super_duper_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    super_duper_api_key = get_settings().intric_super_duper_api_key

    if super_duper_api_key == api_key_header:
        return api_key_header
    else:
        raise AuthenticationException("Unauthorized")