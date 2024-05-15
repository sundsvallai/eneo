from uuid import UUID

from instorage.jobs.job_manager import job_manager
from instorage.jobs.job_models import Job, JobStatus, JobUpdate, Task
from instorage.jobs.job_repo import JobRepository
from instorage.jobs.task_models import TaskParams
from instorage.main.exceptions import NotFoundException
from instorage.users.user import UserInDB


class JobService:
    def __init__(
        self,
        user: UserInDB,
        job_repo: JobRepository,
    ):
        self.user = user
        self.job_repo = job_repo

    async def queue_job(self, task: Task, *, name: str, task_params: TaskParams):
        job = Job(task=task, name=name, status=JobStatus.QUEUED, user_id=self.user.id)
        job_in_db = await self.job_repo.add_job(job=job)

        await job_manager.enqueue(task, job_in_db.uuid, task_params)

        return job_in_db

    async def set_status(self, job_id: UUID, status: JobStatus):
        job_update = JobUpdate(status=status)

        return await self.job_repo.update_job(job_id, job_update)

    async def complete_job(self, job_id: UUID, result_location: str):
        job_update = JobUpdate(
            status=JobStatus.COMPLETE, result_location=result_location
        )

        return await self.job_repo.update_job(job_id, job_update)

    async def get_jobs(self, include_completed: bool = False):
        return await self.job_repo.get_jobs(
            self.user.id, include_completed=include_completed
        )

    async def get_job(self, job_id: UUID):
        job = await self.job_repo.get_job(job_id)

        if job is None or job.user_id != self.user.id:
            raise NotFoundException()

        return job
