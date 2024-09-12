from typing import Optional
from urllib.parse import urlparse
from uuid import UUID

from instorage.ai_models.ai_models_service import AIModelsService
from instorage.jobs.task_service import TaskService
from instorage.main.exceptions import (
    AuthenticationException,
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from instorage.roles.permissions import (
    Permission,
    validate_permission,
    validate_permissions,
)
from instorage.spaces.space import SpacePermissionsActions
from instorage.spaces.space_service import SpaceService
from instorage.users.user import UserInDB
from instorage.websites.crawl_dependencies.crawl_models import (
    CrawlRun,
    CrawlRunCreate,
    CrawlRunUpdate,
    CrawlType,
)
from instorage.websites.crawl_dependencies.crawl_runs_repo import CrawlRunRepository
from instorage.websites.website_models import (
    UpdateInterval,
    Website,
    WebsiteCreate,
    WebsiteCreateRequest,
    WebsiteUpdate,
    WebsiteUpdateRequest,
)
from instorage.websites.website_repo import WebsiteRepository


class WebsiteService:
    def __init__(
        self,
        user: UserInDB,
        repo: WebsiteRepository,
        crawl_run_repo: CrawlRunRepository,
        task_service: TaskService,
        ai_models_service: AIModelsService,
        space_service: SpaceService,
    ):
        self.user = user
        self.repo = repo
        self.crawl_run_repo = crawl_run_repo
        self.task_service = task_service
        self.ai_models_service = ai_models_service
        self.space_service = space_service

    def _validate(self, entity: Website | CrawlRun | None):
        if entity is None:
            raise NotFoundException()

        if entity.tenant_id != self.user.tenant_id:
            raise AuthenticationException()

    async def _check_space_permissions(
        self,
        website: Website,
        action: SpacePermissionsActions = SpacePermissionsActions.READ,
    ):
        space = await self.space_service.get_space(website.space_id)

        match action:
            case SpacePermissionsActions.READ:
                if not space.can_read_resource(self.user):
                    raise NotFoundException()

            case SpacePermissionsActions.EDIT:
                if not space.can_read_resource(self.user):
                    raise NotFoundException()

                if not space.can_edit_resource(self.user):
                    raise UnauthorizedException()

            case SpacePermissionsActions.DELETE:
                if not space.can_read_resource(self.user):
                    raise NotFoundException()

                if not space.can_delete_resource(self.user, website.user_id):
                    raise UnauthorizedException()

    async def check_permissions(
        self,
        website: Website,
        action: SpacePermissionsActions = SpacePermissionsActions.READ,
    ):
        if website.space_id is not None:
            await self._check_space_permissions(website=website, action=action)

        elif self.user.id != website.user_id:
            if action in [
                SpacePermissionsActions.EDIT,
                SpacePermissionsActions.DELETE,
            ]:
                validate_permission(self.user, Permission.EDITOR)

    @validate_permissions(Permission.WEBSITES)
    async def create_website(self, website_create_req: WebsiteCreateRequest):

        website_create = WebsiteCreate(
            **website_create_req.model_dump(),
            user_id=self.user.id,
            tenant_id=self.user.tenant_id,
            embedding_model_id=website_create_req.embedding_model.id,
        )

        website = await self.repo.add(website_create)

        crawl_run = await self.crawl_run_repo.add(
            CrawlRunCreate(website_id=website.id, tenant_id=self.user.tenant_id)
        )

        crawl_job = await self.task_service.queue_crawl(
            name=website.name,
            run_id=crawl_run.id,
            website_id=website.id,
            url=website.url,
            download_files=website.download_files,
            crawl_type=website.crawl_type,
        )

        crawl_run_updated = await self.crawl_run_repo.update(
            CrawlRunUpdate(id=crawl_run.id, job_id=crawl_job.id)
        )
        website.latest_crawl = crawl_run_updated

        return website

    async def create_space_website(
        self,
        url: str,
        space_id: UUID,
        download_files: bool,
        crawl_type: CrawlType,
        update_interval: UpdateInterval,
        name: Optional[str] = None,
        embedding_model_id: Optional[UUID] = None,
    ):
        space = await self.space_service.get_space(space_id)
        if embedding_model_id is None:
            if space.is_personal():
                embedding_model = (
                    await self.ai_models_service.get_latest_available_embedding_model()
                )
            else:
                embedding_model = space.get_latest_embedding_model()

            if embedding_model is None:
                raise BadRequestException(
                    "Can not create a website in a space that does not have "
                    "an embedding model enabled"
                )

            embedding_model_id = embedding_model.id

        elif not space.is_embedding_model_in_space(embedding_model_id):
            raise UnauthorizedException("Embedding model is not available in the space")

        if not space.can_create_websites(self.user):
            raise UnauthorizedException(
                "User does not have permission to create websites in this space"
            )

        website_create = WebsiteCreate(
            space_id=space_id,
            name=name or urlparse(url).netloc,
            url=url,
            download_files=download_files,
            crawl_type=crawl_type,
            update_interval=update_interval,
            user_id=self.user.id,
            tenant_id=self.user.tenant_id,
            embedding_model_id=embedding_model_id,
        )

        website = await self.repo.add(website_create)

        crawl_run = await self.crawl_run_repo.add(
            CrawlRunCreate(website_id=website.id, tenant_id=self.user.tenant_id)
        )

        crawl_job = await self.task_service.queue_crawl(
            name=website.name,
            run_id=crawl_run.id,
            website_id=website.id,
            url=website.url,
            download_files=website.download_files,
            crawl_type=website.crawl_type,
        )

        crawl_run_updated = await self.crawl_run_repo.update(
            CrawlRunUpdate(id=crawl_run.id, job_id=crawl_job.id)
        )
        website.latest_crawl = crawl_run_updated

        return website

    async def get_website(self, id: UUID) -> Website:
        website = await self.repo.get(id)

        self._validate(website)
        await self.check_permissions(website=website)

        return website

    async def get_websites_by_ids(self, ids: list[UUID]) -> list[Website]:
        websites = await self.repo.get_by_ids(ids)

        for website in websites:
            self._validate(website)
            await self.check_permissions(website=website)

        return websites

    async def get_websites(self, by_tenant: bool = False) -> list[Website]:
        if by_tenant:
            validate_permission(self.user, permission=Permission.ADMIN)
            websites = await self.repo.get_by_tenant(self.user.tenant.id)
        else:
            websites = await self.repo.get_by_user(self.user.id)

        return websites

    async def update_website(
        self, website_update_req: WebsiteUpdateRequest, website_id: UUID
    ):
        website_update = WebsiteUpdate(
            **website_update_req.model_dump(exclude_unset=True), id=website_id
        )
        website = await self.repo.update(website_update)

        self._validate(website)
        await self.check_permissions(
            website=website, action=SpacePermissionsActions.EDIT
        )

        return website

    async def delete_website(self, website_id: UUID):
        # Runs validation
        website = await self.get_website(website_id)

        await self.check_permissions(
            website=website, action=SpacePermissionsActions.DELETE
        )

        return await self.repo.delete(website_id)

    async def get_crawl_runs(self, website_id: UUID):
        website = await self.get_website(website_id)
        runs = await self.crawl_run_repo.get_by_website(website.id)

        for run in runs:
            self._validate(run)

        return runs

    async def get_crawl_run(self, id: UUID):
        run = await self.crawl_run_repo.get(id)

        self._validate(run)

        return run

    async def move_website_to_space(
        self, website_id: UUID, space_id: UUID, assistant_ids: list[UUID] = []
    ):
        space = await self.space_service.get_space(space_id)
        website = await self.get_website(website_id)

        if website.space_id is not None:
            source_space = await self.space_service.get_space(website.space_id)

            if not source_space.can_delete_resource(self.user, website.user_id):
                raise UnauthorizedException(
                    "User does not have permission to move website from space"
                )

        if not space.can_create_websites(self.user):
            raise UnauthorizedException(
                "User does not have permission to create websites in the space"
            )

        if not space.is_embedding_model_in_space(website.embedding_model_id):
            raise BadRequestException(
                f"Space does not have embedding model {website.embedding_model.name} enabled."
            )

        await self.repo.add_website_to_space(website_id=website_id, space_id=space_id)
        await self.repo.remove_website_from_all_assistants(
            website_id=website_id, assistant_ids=assistant_ids
        )
