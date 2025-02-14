import contextlib
import os
from pathlib import Path
from uuid import UUID

from intric.jobs.task_models import Transcription, UploadInfoBlob
from intric.main.container.container import Container
from intric.worker.dependencies.worker_container_overrides import (
    override_embedding_model_from_group,
)


def _remove_file(filepath: Path):
    with contextlib.suppress(FileNotFoundError):
        os.remove(filepath)


async def transcription_task(
    *,
    job_id: UUID,
    params: Transcription,
    container: Container,
):
    task_manager = container.task_manager(job_id=job_id)
    async with task_manager.set_status_on_exception():
        await override_embedding_model_from_group(
            container=container, group_id=params.group_id
        )

        filepath = Path(params.filepath)

        # Define cleanup function
        task_manager.cleanup_func = lambda: _remove_file(filepath)

        transcriber = container.transcriber()
        uploader = container.text_processor()

        text = await transcriber.transcribe_from_filepath(filepath=filepath)
        info_blob = await uploader.process_text(
            text=text, title=params.filename, group_id=params.group_id
        )

        task_manager.result_location = f"/api/v1/info-blobs/{info_blob.id}/"

    return task_manager.successful()


async def upload_info_blob_task(
    *,
    job_id: UUID,
    params: UploadInfoBlob,
    container: Container,
):
    task_manager = container.task_manager(job_id=job_id)
    async with task_manager.set_status_on_exception():
        await override_embedding_model_from_group(
            container=container, group_id=params.group_id
        )

        filepath = Path(params.filepath)

        # Define cleanup function
        task_manager.cleanup_func = lambda: _remove_file(filepath)

        uploader = container.text_processor()

        info_blob = await uploader.process_file(
            filepath=filepath,
            filename=params.filename,
            mimetype=params.mimetype,
            group_id=params.group_id,
        )

        task_manager.result_location = f"/api/v1/info-blobs/{info_blob.id}/"

    return task_manager.successful()
