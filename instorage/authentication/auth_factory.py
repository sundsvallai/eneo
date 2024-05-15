from fastapi import Depends

from instorage.authentication.api_key_repo import ApiKeysRepository
from instorage.authentication.auth_service import AuthService
from instorage.server.dependencies.db import get_repository


def get_auth_service(
    api_key_repo: ApiKeysRepository = Depends(get_repository(ApiKeysRepository)),
):
    return AuthService(api_key_repo=api_key_repo)
