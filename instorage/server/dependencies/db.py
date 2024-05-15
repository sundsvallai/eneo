from typing import Callable, Type

from fastapi import Depends

from instorage.database.database import AsyncSession, sessionmanager
from instorage.database.repositories.base import BaseRepositoryDelegate


async def get_session():
    async with sessionmanager.session() as session, session.begin():
        yield session


def get_repository(Repo_type: Type) -> Callable:
    def get_repo(
        db: AsyncSession = Depends(get_session),
    ) -> Type[BaseRepositoryDelegate]:
        return Repo_type(db)

    return get_repo
