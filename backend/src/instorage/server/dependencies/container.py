from uuid import UUID

from dependency_injector import providers
from fastapi import Depends, Security

from instorage.database.database import AsyncSession, get_session
from instorage.main.container.container import Container
from instorage.main.container.container_overrides import override_user
from instorage.server.dependencies.auth_definitions import API_KEY_HEADER, OAUTH2_SCHEME
from instorage.users.setup import setup_user


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

        if not user.is_active:
            await setup_user(container=container)

        override_user(container=container, user=user)

        return container

    async def _get_container_with_user_from_assistant_api_key(
        id: UUID,
        token: str = Security(OAUTH2_SCHEME),
        api_key: str = Security(API_KEY_HEADER),
        container: Container = Depends(_get_container),
    ):
        user = await container.user_service().authenticate_with_assistant_api_key(
            token=token, api_key=api_key, assistant_id=id
        )
        override_user(container=container, user=user)

        return container

    if with_user:
        return _get_container_with_user

    if with_user_from_assistant_api_key:
        return _get_container_with_user_from_assistant_api_key

    return _get_container
