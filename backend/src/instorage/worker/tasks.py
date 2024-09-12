import contextlib
import os
from pathlib import Path

from instorage.jobs.task_models import Transcription, UploadInfoBlob
from instorage.main.container.container import Container
from instorage.worker.task_manager import TaskManager
from instorage.worker.worker_factory import task


def _remove_file(filepath: Path):
    with contextlib.suppress(FileNotFoundError):
        os.remove(filepath)


@task
async def transcription_task(
    *,
    params: Transcription,
    container: Container,
    task_manager: TaskManager,
):
    filepath = Path(params.filepath)

    # Define cleanup function
    task_manager.cleanup_func = lambda: _remove_file(filepath)

    transcriber = container.transcriber()
    uploader = container.text_processor()

    text = await transcriber.transcribe(filepath=filepath)
    info_blob = await uploader.process_text(
        text=text, title=params.filename, group_id=params.group_id
    )

    return f"/api/v1/info-blobs/{info_blob.id}/"


@task
async def upload_info_blob_task(
    *,
    params: UploadInfoBlob,
    container: Container,
    task_manager: TaskManager,
):
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

    return f"/api/v1/info-blobs/{info_blob.id}/"
