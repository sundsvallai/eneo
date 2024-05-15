from dependency_injector import providers
from fastapi import Depends, Security

from instorage.database.database import AsyncSession
from instorage.main.container import Container
from instorage.server.dependencies.auth_definitions import API_KEY_HEADER, OAUTH2_SCHEME
from instorage.server.dependencies.db import get_session


def get_container(
    with_user: bool = False,
    with_user_from_assistant_api_key: bool = False,
):

    async def _get_container(
        session: AsyncSession = Depends(get_session),
    ):
        return Container(
            session=providers.Object(session),
        )

    async def _get_container_with_user(
        token: str = Security(OAUTH2_SCHEME),
        api_key: str = Security(API_KEY_HEADER),
        container: Container = Depends(_get_container),
    ):
        user = await container.user_service().authenticate(token=token, api_key=api_key)
        container.user.override(providers.Object(user))
        container.tenant.override(providers.Object(user.tenant))

        return container

    async def _get_container_with_user_from_assistant_api_key(
        token: str = Security(OAUTH2_SCHEME),
        api_key: str = Security(API_KEY_HEADER),
        container: Container = Depends(_get_container),
    ):
        user = await container.user_service().authenticate_with_assistant_api_key(
            token=token, api_key=api_key
        )
        container.user.override(providers.Object(user))
        container.tenant.override(providers.Object(user.tenant))

        return container

    if with_user:
        return _get_container_with_user

    if with_user_from_assistant_api_key:
        return _get_container_with_user_from_assistant_api_key

    return _get_container
