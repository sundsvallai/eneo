import sqlalchemy as sa

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.job_table import Jobs
from instorage.jobs.job_models import Job, JobInDb, JobStatus, JobUpdate


class JobRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            Jobs,
            JobInDb,
        )

    async def add_job(self, job: Job):
        return await self.delegate.add(job)

    async def update_job(self, uuid: str, job: JobUpdate):
        stmt = (
            sa.update(Jobs)
            .values(job.model_dump(exclude_unset=True))
            .where(Jobs.uuid == uuid)
            .returning(Jobs)
        )

        return await self.delegate.get_model_from_query(stmt)

    async def get_job(self, uuid: str):
        return await self.delegate.get_by(conditions={Jobs.uuid: uuid})

    async def get_jobs(self, user_id: int, include_completed: bool):
        stmt = sa.select(Jobs).where(Jobs.user_id == user_id).order_by(Jobs.created_at)

        if not include_completed:
            stmt = stmt.where(Jobs.status != JobStatus.COMPLETE)

        return await self.delegate.get_models_from_query(stmt)
