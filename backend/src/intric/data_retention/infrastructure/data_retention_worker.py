from intric.main.container.container import Container
from intric.worker.worker import Worker

worker = Worker()


@worker.cron_job(hour=3, minute=0)  # Run daily at 3 AM
async def cleanup_old_data(container: Container):
    data_retention_service = container.data_retention_service()

    async with container.session().begin():
        await data_retention_service.delete_old_questions()
        await data_retention_service.delete_old_app_runs()
        await data_retention_service.delete_old_sessions()
    return True
