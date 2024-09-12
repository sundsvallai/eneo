from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.jobs import job_factory
from instorage.jobs.job_models import JobPublic
from instorage.jobs.job_service import JobService
from instorage.main.models import PaginatedResponse
from instorage.server import protocol

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[JobPublic])
async def get_jobs(
    include_completed: bool = False,
    job_service: JobService = Depends(job_factory.get_job_service),
):
    jobs = await job_service.get_jobs(include_completed)

    return protocol.to_paginated_response(jobs)


@router.get("/{id}/", response_model=JobPublic)
async def get_job(
    id: UUID, job_service: JobService = Depends(job_factory.get_job_service)
):
    return await job_service.get_job(id)
