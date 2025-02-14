from uuid import UUID

from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

from intric.jobs.job_models import Task
from intric.jobs.task_models import TaskParams
from intric.main.config import get_settings
from intric.main.exceptions import NotReadyException
from intric.main.logging import get_logger

logger = get_logger(__name__)


class JobManager:
    def __init__(self):
        self._redis: ArqRedis | None = None

    async def init(self):
        self._redis = await create_pool(
            RedisSettings(
                host=get_settings().redis_host, port=get_settings().redis_port
            )
        )

        logger.debug(
            f"Job manager connected to redis on host {get_settings().redis_host}"
            f" and port {get_settings().redis_port}"
        )

    async def close(self):
        await self._redis.aclose()

    async def enqueue(self, task: Task, job_id: UUID, params: TaskParams):
        if self._redis is None:
            raise NotReadyException("Job manager is not initialized!")

        await self._redis.enqueue_job(task, params, _job_id=str(job_id))

    async def enqueue_jobless(self, task: Task):
        await self._redis.enqueue_job(task)


job_manager = JobManager()
