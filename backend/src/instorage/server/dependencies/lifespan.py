from contextlib import asynccontextmanager

from fastapi import FastAPI

from instorage.database.database import sessionmanager
from instorage.jobs.job_manager import job_manager
from instorage.main.aiohttp_client import aiohttp_client
from instorage.main.config import SETTINGS
from instorage.server.dependencies.ai_models import init_models
from instorage.server.dependencies.modules import init_modules
from instorage.server.dependencies.predefined_roles import init_predefined_roles


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


async def startup():
    aiohttp_client.start()
    sessionmanager.init(SETTINGS.database_url)
    await job_manager.init()

    # init predefined roles
    await init_predefined_roles()

    # init models
    await init_models()

    # init modules
    await init_modules()


async def shutdown():
    await sessionmanager.close()
    await aiohttp_client.stop()
    await job_manager.close()
