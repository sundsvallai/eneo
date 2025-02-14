from uuid import UUID

from dependency_injector import providers

from intric.main.container.container import Container
from intric.main.logging import get_logger
from intric.websites.crawl_dependencies.crawl_models import (
    CrawlRunCreate,
    CrawlRunUpdate,
    CrawlTask,
)
from intric.websites.website_models import UpdateInterval
from intric.worker.dependencies.worker_container_overrides import (
    override_embedding_model_from_website,
)

logger = get_logger(__name__)


async def queue_website_crawls(container: Container):
    user_repo = container.user_repo()
    crawl_run_repo = container.crawl_run_repo()

    async with container.session().begin():
        websites = await container.website_repo().get_all()

        for website in websites:
            try:
                if website.update_interval == UpdateInterval.WEEKLY:
                    # Get user
                    user = await user_repo.get_user_by_id(website.user_id)
                    container.user.override(providers.Object(user))
                    container.tenant.override(providers.Object(user.tenant))

                    # Create crawl run
                    crawl_run = await crawl_run_repo.add(
                        CrawlRunCreate(website_id=website.id, tenant_id=user.tenant_id)
                    )
                    crawl_job = await container.task_service().queue_crawl(
                        name=website.name,
                        run_id=crawl_run.id,
                        website_id=website.id,
                        url=website.url,
                        download_files=website.download_files,
                        crawl_type=website.crawl_type,
                    )

                    await crawl_run_repo.update(
                        CrawlRunUpdate(id=crawl_run.id, job_id=crawl_job.id)
                    )
            except Exception as e:
                # If a website fails to queue, try the next one
                logger.error(f"Error when queueing up website {website.url}: {e}")

    return True


async def crawl_task(*, job_id: UUID, params: CrawlTask, container: Container):
    task_manager = container.task_manager(job_id=job_id)
    async with task_manager.set_status_on_exception():
        await override_embedding_model_from_website(
            container=container,
            website_id=params.website_id,
            tenant_id=container.user().tenant_id,
        )

        # Get resources
        crawler = container.crawler()
        uploader = container.text_processor()
        crawl_run_repo = container.crawl_run_repo()

        info_blob_repo = container.info_blob_repo()
        website_service = container.website_service()

        # Do task
        logger.info(f"Running crawl with params: {params}")
        num_pages = 0
        num_files = 0
        num_̈́failed_pages = 0
        num_failed_files = 0
        num_deleted_blobs = 0

        # Unfortunately, in this type of background task we still need to care about the session atm
        session = container.session()

        existing_titles = await info_blob_repo.get_titles_of_website(params.website_id)

        crawled_titles = []

        async with crawler.crawl(
            url=params.url,
            download_files=params.download_files,
            crawl_type=params.crawl_type,
        ) as crawl:
            for page in crawl.pages:
                num_pages += 1
                try:
                    title = page.url
                    async with session.begin_nested():
                        await uploader.process_text(
                            text=page.content,
                            title=title,
                            website_id=params.website_id,
                            url=page.url,
                        )
                    crawled_titles.append(title)

                except Exception:
                    logger.exception("Exception while uploading page")
                    num_̈́failed_pages += 1

            for file in crawl.files:
                num_files += 1
                try:
                    filename = file.stem
                    async with session.begin_nested():
                        await uploader.process_file(
                            filepath=file,
                            filename=filename,
                            website_id=params.website_id,
                        )

                    crawled_titles.append(filename)
                except Exception:
                    logger.exception("Exception while uploading file")
                    num_failed_files += 1

            for title in existing_titles:
                if title not in crawled_titles:
                    num_deleted_blobs += 1
                    await info_blob_repo.delete_by_title_and_website(
                        title=title, website_id=params.website_id
                    )

            await website_service.update_website_size(params.website_id)

            logger.info(
                f"Crawler finished. {num_pages} pages, {num_̈́failed_pages} failed. "
                f"{num_files} files, {num_failed_files} failed. "
                f"{num_deleted_blobs} blobs deleted."
            )

            await crawl_run_repo.update(
                CrawlRunUpdate(
                    id=params.run_id,
                    pages_crawled=num_pages,
                    files_downloaded=num_files,
                    pages_failed=num_̈́failed_pages,
                    files_failed=num_failed_files,
                )
            )

        task_manager.result_location = (
            f"/api/v1/websites/{params.website_id}/info-blobs/"
        )

    return task_manager.successful()
