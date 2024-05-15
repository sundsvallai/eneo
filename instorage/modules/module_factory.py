from fastapi import Depends

from instorage.modules.module_repo import ModuleRepository
from instorage.server.dependencies.db import get_session


def get_module_repo(db=Depends(get_session)):
    return ModuleRepository(db)
