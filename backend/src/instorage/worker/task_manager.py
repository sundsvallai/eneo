import asyncio
from contextlib import asynccontextmanager
from typing import Callable
from uuid import UUID

from instorage.database.database import AsyncSession
from instorage.jobs.job_models import JobStatus
from instorage.jobs.job_service import JobService
from instorage.main.logging import get_logger

logger = get_logger(__name__)


class TaskManager:
    def __init__(
        self,
        job_id: UUID,
        session: AsyncSession,
        job_service: JobService,
    ):
        self.job_id = job_id
        self.session = session
        self.job_service = job_service

        self.success = None
        self._result_location = None
        self._cleanup_func = None

    @property
    def result_location(self):
        return self._result_location

    @result_location.setter
    def result_location(self, result_location: str):
        self._result_location = result_location

    @property
    def cleanup_func(self):
        return self._cleanup_func

    @cleanup_func.setter
    def cleanup_func(self, cleanup_func: Callable):
        self._cleanup_func = cleanup_func

    def _log_status(self, status: JobStatus):
        logger.info(f"Status for {self.job_id}: {status}")

    @asynccontextmanager
    async def set_status_on_exception(self):
        await self.set_status(JobStatus.IN_PROGRESS)

        try:
            yield
        except (Exception, asyncio.CancelledError):
            logger.exception("Error on worker:")
            await self.fail_job()
            self.success = False
        else:
            await self.complete_job()
            self.success = True
        finally:
            if self._cleanup_func is not None:
                self._cleanup_func()

    def successful(self):
        return self.success

    async def set_status(self, status: JobStatus):
        self._log_status(status)

        async with self.session.begin():
            await self.job_service.set_status(self.job_id, status)

    async def complete_job(self):
        async with self.session.begin():
            await self.job_service.complete_job(self.job_id, self._result_location)

    async def fail_job(self):
        async with self.session.begin():
            await self.job_service.fail_job(self.job_id)
