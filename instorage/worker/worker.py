import crochet
from arq.connections import RedisSettings

from instorage.jobs.task_models import Transcription, UploadInfoBlob
from instorage.main.config import get_settings
from instorage.main.logging import get_logger
from instorage.server.dependencies import lifespan
from instorage.worker.tasks import transcription_task, upload_info_blob_task
from instorage_prop.crawler.crawl_models import CrawlTask

logger = get_logger(__name__)


async def startup(ctx):
    await lifespan.startup()
    crochet.setup()


async def shutdown(ctx):
    await lifespan.shutdown()


async def upload_info_blob(ctx, params: UploadInfoBlob):
    job_id = ctx['job_id']

    return await upload_info_blob_task(job_id=job_id, params=params)


async def transcription(ctx, params: Transcription):
    job_id = ctx['job_id']

    return await transcription_task(job_id=job_id, params=params)


functions = [upload_info_blob, transcription]

if get_settings().using_intric_proprietary:
    from instorage.jobs.task_models import EmbedGroup
    from instorage_prop.worker.tasks import crawl_task, embed_group_task

    async def crawl(ctx, params: CrawlTask):
        job_id = ctx['job_id']

        return await crawl_task(job_id=job_id, params=params)

    async def embed_group(ctx, params: EmbedGroup):
        job_id = ctx['job_id']

        return await embed_group_task(job_id=job_id, params=params)

    functions.extend([crawl, embed_group])


class WorkerSettings:
    functions = functions
    redis_settings = RedisSettings(
        host=get_settings().redis_host, port=get_settings().redis_port
    )
    on_startup = startup
    on_shutdown = shutdown
    retry_jobs = False
    job_timeout = 60 * 60 * 24  # High timeout that is effectively not a timeout
    max_jobs = 10  # Maximum number of jobs to run at a time
