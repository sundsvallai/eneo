from typing import Callable, Type

from fastapi import Depends

from instorage.database.database import AsyncSession, get_session
from instorage.database.repositories.base import BaseRepositoryDelegate


def get_repository(Repo_type: Type) -> Callable:
    def get_repo(
        db: AsyncSession = Depends(get_session),
    ) -> Type[BaseRepositoryDelegate]:
        return Repo_type(db)

    return get_repo
