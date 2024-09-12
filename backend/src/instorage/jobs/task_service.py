import asyncio
from tempfile import SpooledTemporaryFile
from uuid import UUID

from instorage.files.audio import AudioMimeTypes
from instorage.files.file_size_service import FileSizeService
from instorage.files.text import TextMimeTypes
from instorage.groups.group import GroupInDB
from instorage.groups.group_service import GroupService
from instorage.jobs.job_models import JobInDb, Task
from instorage.jobs.job_service import JobService
from instorage.jobs.task_models import EmbedGroup, Transcription, UploadInfoBlob
from instorage.main.config import get_settings
from instorage.main.exceptions import FileNotSupportedException, FileTooLargeException
from instorage.users.user import UserInDB
from instorage.websites.crawl_dependencies.crawl_models import CrawlTask, CrawlType


class TaskService:
    def __init__(
        self,
        user: UserInDB,
        group_service: GroupService,
        file_size_service: FileSizeService,
        job_service: JobService,
    ):
        self.user = user
        self.group_service = group_service
        self.file_size_service = file_size_service
        self.job_service = job_service

    @staticmethod
    def get_task_type(mimetype: str):
        if TextMimeTypes.has_value(mimetype):
            return Task.UPLOAD_FILE
        elif AudioMimeTypes.has_value(mimetype):
            return Task.TRANSCRIPTION
        else:
            raise FileNotSupportedException(f"{mimetype} not supported.")

    @staticmethod
    def get_max_size(task: Task):
        match task:
            case Task.UPLOAD_FILE:
                return get_settings().upload_max_file_size
            case Task.TRANSCRIPTION:
                return get_settings().transcription_max_file_size
            case _:
                return 0

    async def validate_file_size(self, file: SpooledTemporaryFile, task: Task):
        max_size = self.get_max_size(task)

        if await asyncio.to_thread(self.file_size_service.is_too_large, file, max_size):
            raise FileTooLargeException("File too large.")

    async def queue_upload_file(
        self, group_id: UUID, file: SpooledTemporaryFile, mimetype: str, filename: str
    ):
        task_type = self.get_task_type(mimetype)

        # Validate group
        group = await self.group_service.get_group(group_id)
        if group.space_id is not None:
            await self.group_service.check_space_embedding_model(group)

        await self.validate_file_size(file, task_type)

        filepath = await self.file_size_service.save_file_to_disk(file)

        if task_type == Task.UPLOAD_FILE:
            params = UploadInfoBlob(
                filepath=filepath,
                filename=filename,
                user_id=self.user.id,
                group_id=group.id,
                mimetype=mimetype,
            )
        elif task_type == Task.TRANSCRIPTION:
            params = Transcription(
                filepath=filepath,
                filename=filename,
                user_id=self.user.id,
                group_id=group.id,
                mimetype=mimetype,
            )

        # Set name of the job to the filename being processed
        job = await self.job_service.queue_job(
            task_type, name=filename, task_params=params
        )

        return job

    async def queue_crawl(
        self,
        name: str,
        run_id: UUID,
        url: str,
        download_files: bool = False,
        crawl_type: CrawlType = CrawlType.CRAWL,
        website_id: UUID | None = None,
        group_id: UUID | None = None,
    ) -> JobInDb:
        params = CrawlTask(
            user_id=self.user.id,
            run_id=run_id,
            url=url,
            download_files=download_files,
            crawl_type=crawl_type,
            website_id=website_id,
            group_id=group_id,
        )

        return await self.job_service.queue_job(
            Task.CRAWL, name=name, task_params=params
        )

    async def queue_re_embed_group(self, group: GroupInDB):
        # Set name
        name = f"Re-embed {group.name}"

        # Set params
        params = EmbedGroup(user_id=self.user.id, group_id=group.id)

        return await self.job_service.queue_job(
            Task.EMBED_GROUP, name=name, task_params=params
        )
