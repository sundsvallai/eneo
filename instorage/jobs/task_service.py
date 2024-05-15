import asyncio
from tempfile import SpooledTemporaryFile
from typing import Optional
from uuid import UUID

from instorage.groups.group import GroupInDB
from instorage.groups.group_service import GroupService
from instorage.info_blobs.file.file_service import FileService
from instorage.info_blobs.file.text import AUDIO_FILE_TYPES, TextMimeTypes
from instorage.jobs.job_models import Task
from instorage.jobs.job_service import JobService
from instorage.jobs.task_models import EmbedGroup, Transcription, UploadInfoBlob
from instorage.main.exceptions import FileNotSupportedException, FileTooLargeException
from instorage.users.user import UserInDB
from instorage_prop.crawler.crawl_models import CrawlTask, CrawlType

UPLOAD_MAX_FILE_SIZE = 1024**2 * 10  # 10MB
TRANSCRIPTION_MAX_FILE_SIZE = 1024**2 * 200  # 200MB


class TaskService:
    def __init__(
        self,
        user: UserInDB,
        group_service: GroupService,
        file_service: FileService,
        job_service: JobService,
    ):
        self.user = user
        self.group_service = group_service
        self.file_service = file_service
        self.job_service = job_service

    @staticmethod
    def get_task_type(mimetype: str):
        if TextMimeTypes.has_value(mimetype):
            return Task.UPLOAD_FILE
        elif mimetype in AUDIO_FILE_TYPES:
            return Task.TRANSCRIPTION
        else:
            raise FileNotSupportedException(f"{mimetype} not supported.")

    @staticmethod
    def get_max_size(task: Task):
        match task:
            case Task.UPLOAD_FILE:
                return UPLOAD_MAX_FILE_SIZE
            case Task.TRANSCRIPTION:
                return TRANSCRIPTION_MAX_FILE_SIZE
            case _:
                return 0

    async def validate_file_size(self, file: SpooledTemporaryFile, task: Task):
        max_size = self.get_max_size(task)

        if await asyncio.to_thread(self.file_service.is_too_large, file, max_size):
            raise FileTooLargeException("File too large.")

    async def queue_upload_file(
        self, group_id: UUID, file: SpooledTemporaryFile, mimetype: str, filename: str
    ):
        task_type = self.get_task_type(mimetype)

        # Validate group
        group = await self.group_service.get_group_by_uuid(group_id)

        await self.validate_file_size(file, task_type)

        filepath = await self.file_service.save_file_to_disk(file)

        if task_type == Task.UPLOAD_FILE:
            params = UploadInfoBlob(
                filepath=filepath,
                filename=filename,
                user_id=self.user.uuid,
                group_id=group.uuid,
            )
        elif task_type == Task.TRANSCRIPTION:
            params = Transcription(
                filepath=filepath,
                filename=filename,
                user_id=self.user.uuid,
                group_id=group.uuid,
            )

        # Set name of the job to the filename being processed
        job = await self.job_service.queue_job(
            task_type, name=filename, task_params=params
        )

        return job

    async def queue_crawl(
        self,
        name: str,
        group_id: UUID,
        url: str,
        allowed_path: Optional[str] = None,
        download_files: bool = False,
        crawl_type: CrawlType = CrawlType.CRAWL,
    ):

        # Validate group
        await self.group_service.get_group_by_uuid(group_id)
        params = CrawlTask(
            user_id=self.user.uuid,
            group_id=group_id,
            url=url,
            allowed_path=allowed_path,
            download_files=download_files,
            crawl_type=crawl_type,
        )

        return await self.job_service.queue_job(
            Task.CRAWL, name=name, task_params=params
        )

    async def queue_re_embed_group(self, group: GroupInDB):
        # Set name
        name = f"Re-embed {group.name}"

        # Set params
        params = EmbedGroup(user_id=self.user.uuid, group_id=group.uuid)

        return await self.job_service.queue_job(
            Task.EMBED_GROUP, name=name, task_params=params
        )
