from dependency_injector import containers, providers

from instorage.admin.admin_service import AdminService
from instorage.admin.quota_service import QuotaService
from instorage.ai_models.completion_models.completion_models_repo import (
    CompletionModelsRepository,
)
from instorage.ai_models.embedding_models.datastore.datastore import Datastore
from instorage.ai_models.embedding_models.embedding_model_adapters.multilingual_e5_large import (
    MultilingualE5LargeAdapter,
)
from instorage.ai_models.embedding_models.embedding_model_adapters.text_embedding_openai import (
    OpenAIEmbeddingAdapter,
)
from instorage.ai_models.embedding_models.embedding_models import (
    EmbeddingModel,
    ModelFamily,
)
from instorage.ai_models.transcription_models.model_adapters.whisper import (
    OpenAISTTModelAdapter,
)
from instorage.allowed_origins.allowed_origin_repo import AllowedOriginRepository
from instorage.allowed_origins.allowed_origin_service import AllowedOriginService
from instorage.analysis.analysis_repo import AnalysisRepository
from instorage.analysis.analysis_service import AnalysisService
from instorage.assistants.assistant_repo import AssistantRepository
from instorage.assistants.assistant_service import AssistantService
from instorage.authentication.api_key_repo import ApiKeysRepository
from instorage.authentication.auth_service import AuthService
from instorage.database.database import AsyncSession
from instorage.groups.group_repo import GroupRepository
from instorage.groups.group_service import GroupService
from instorage.info_blobs.file.file_service import FileService
from instorage.info_blobs.file.text import TextExtractor
from instorage.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.info_blobs.info_blob_service import InfoBlobService
from instorage.info_blobs.text_processor import TextProcessor
from instorage.info_blobs.transcriber import Transcriber
from instorage.jobs.job_repo import JobRepository
from instorage.jobs.job_service import JobService
from instorage.jobs.task_service import TaskService
from instorage.main.config import get_settings
from instorage.predefined_roles.predefined_role_service import PredefinedRolesService
from instorage.predefined_roles.predefined_roles_repo import PredefinedRolesRepository
from instorage.questions.questions_repo import QuestionRepository
from instorage.roles.roles_repo import RolesRepository
from instorage.roles.roles_service import RolesService
from instorage.services.service_repo import ServiceRepository
from instorage.sessions.sessions_repo import SessionRepository
from instorage.settings.setting_service import SettingService
from instorage.settings.settings_repo import SettingsRepository
from instorage.tenants.tenant import TenantInDB
from instorage.tenants.tenant_repo import TenantRepository
from instorage.user_groups.user_groups_repo import UserGroupsRepository
from instorage.user_groups.user_groups_service import UserGroupsService
from instorage.users.user import UserInDB
from instorage.users.user_repo import UsersRepository
from instorage.users.user_service import UserService
from instorage.worker.task_manager import TaskManager
from instorage.workflows.step_repo import StepRepository


class Container(containers.DeclarativeContainer):

    # Configuration
    config = providers.Configuration()

    # Objects
    session = providers.Dependency(instance_of=AsyncSession)
    user = providers.Dependency(instance_of=UserInDB)
    tenant = providers.Dependency(instance_of=TenantInDB)
    embedding_model = providers.Dependency(instance_of=EmbeddingModel)

    # Repositories
    user_repo = providers.Factory(UsersRepository, session=session)
    settings_repo = providers.Factory(SettingsRepository, session=session)
    tenant_repo = providers.Factory(TenantRepository, session=session)
    assistant_repo = providers.Factory(AssistantRepository, session=session)
    api_key_repo = providers.Factory(ApiKeysRepository, session=session)
    group_repo = providers.Factory(GroupRepository, session=session)
    info_blob_repo = providers.Factory(InfoBlobRepository, session=session)
    job_repo = providers.Factory(JobRepository, session=session)
    allowed_origin_repo = providers.Factory(AllowedOriginRepository, session=session)
    predefined_role_repo = providers.Factory(PredefinedRolesRepository, session=session)
    role_repo = providers.Factory(RolesRepository, session=session)
    completion_model_repo = providers.Factory(
        CompletionModelsRepository, session=session
    )
    info_blob_chunk_repo = providers.Factory(InfoBlobChunkRepo, session=session)
    service_repo = providers.Factory(ServiceRepository, session=session)
    step_repo = providers.Factory(StepRepository, session=session)
    user_groups_repo = providers.Factory(UserGroupsRepository, session=session)
    analysis_repo = providers.Factory(AnalysisRepository, session=session)
    session_repo = providers.Factory(SessionRepository, session=session)
    question_repo = providers.Factory(QuestionRepository, session=session)

    # Embedding model adapters
    multilingual_adapter = providers.Factory(
        MultilingualE5LargeAdapter, model=embedding_model
    )
    openai_embedding_adapter = providers.Factory(
        OpenAIEmbeddingAdapter, model=embedding_model
    )
    embedding_model_selector = providers.Selector(
        config.embedding_model,
        **{
            ModelFamily.E5.value: multilingual_adapter,
            ModelFamily.OPEN_AI.value: openai_embedding_adapter,
        }
    )

    # Speech-to-text model adapter
    openai_stt_model_adapter = providers.Factory(OpenAISTTModelAdapter)

    # Datastore
    datastore = providers.Factory(
        Datastore,
        embedding_model_adapter=embedding_model_selector,
        info_blob_chunk_repo=info_blob_chunk_repo,
    )
    extractor = providers.Factory(TextExtractor)

    # Services
    auth_service = providers.Factory(
        AuthService,
        api_key_repo=api_key_repo,
    )
    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
        auth_service=auth_service,
        settings_repo=settings_repo,
        tenant_repo=tenant_repo,
        assistant_repo=assistant_repo,
        predefined_roles_repo=predefined_role_repo,
    )
    group_service = providers.Factory(
        GroupService,
        user=user,
        repo=group_repo,
        tenant_repo=tenant_repo,
        info_blob_repo=info_blob_repo,
    )
    quota_service = providers.Factory(
        QuotaService, user=user, info_blob_repo=info_blob_repo
    )
    info_blob_service = providers.Factory(
        InfoBlobService,
        repo=info_blob_repo,
        user=user,
        quota_service=quota_service,
        group_service=group_service,
    )
    job_service = providers.Factory(
        JobService,
        user=user,
        job_repo=job_repo,
    )
    file_service = providers.Factory(
        FileService,
    )
    task_service = providers.Factory(
        TaskService,
        user=user,
        group_service=group_service,
        file_service=file_service,
        job_service=job_service,
    )
    allowed_origin_service = providers.Factory(
        AllowedOriginService,
        user=user,
        repo=allowed_origin_repo,
    )
    predefined_role_service = providers.Factory(
        PredefinedRolesService, repo=predefined_role_repo
    )
    role_service = providers.Factory(RolesService, user=user, repo=role_repo)
    settings_service = providers.Factory(
        SettingService,
        user=user,
        repo=settings_repo,
    )
    assistant_service = providers.Factory(
        AssistantService,
        user=user,
        repo=assistant_repo,
        auth_service=auth_service,
        service_repo=service_repo,
        step_repo=step_repo,
    )
    user_group_service = providers.Factory(
        UserGroupsService, user=user, repo=user_groups_repo
    )
    admin_service = providers.Factory(
        AdminService,
        user=user,
        user_repo=user_repo,
        tenant_repo=tenant_repo,
        user_service=user_service,
    )
    analysis_service = providers.Factory(
        AnalysisService,
        user=user,
        repo=analysis_repo,
        assistant_repo=assistant_repo,
        session_repo=session_repo,
        question_repo=question_repo,
    )

    # Worker
    task_manager = providers.Factory(
        TaskManager,
        session=session,
        job_service=job_service,
    )
    text_processor = providers.Factory(
        TextProcessor,
        user=user,
        extractor=extractor,
        datastore=datastore,
        info_blob_service=info_blob_service,
        session=session,
    )
    transcriber = providers.Factory(
        Transcriber,
        adapter=openai_stt_model_adapter,
    )

    if get_settings().using_intric_proprietary:
        from instorage_prop.crawler.crawl_repo import CrawlRepository
        from instorage_prop.crawler.crawl_service import CrawlService
        from instorage_prop.crawler.crawler import Crawler
        from instorage_prop.sysadmin.sysadmin_service import SysAdminService

        # Repositories
        crawl_repo = providers.Factory(CrawlRepository, session=session)

        # Services
        crawl_service = providers.Factory(
            CrawlService, user=user, repo=crawl_repo, task_service=task_service
        )
        sysadmin_service = providers.Factory(
            SysAdminService, group_repo=group_repo, task_service=task_service
        )

        # Worker
        crawler = providers.Factory(Crawler)
