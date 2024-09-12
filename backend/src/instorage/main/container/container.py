from dependency_injector import containers, providers

from instorage.admin.admin_service import AdminService
from instorage.admin.quota_service import QuotaService
from instorage.ai_models.ai_models_service import AIModelsService
from instorage.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelFamily,
)
from instorage.ai_models.completion_models.completion_model_adapters.azure_model_adapter import (
    AzureOpenAIModelAdapter,
)
from instorage.ai_models.completion_models.completion_model_adapters.claude_model_adapter import (
    ClaudeModelAdapter,
)
from instorage.ai_models.completion_models.completion_model_adapters.openai_model_adapter import (
    OpenAIModelAdapter,
)
from instorage.ai_models.completion_models.completion_model_adapters.vllm_model_adapter import (
    VLMMModelAdapter,
)
from instorage.ai_models.completion_models.completion_models_repo import (
    CompletionModelsRepository,
)
from instorage.ai_models.completion_models.completion_service import CompletionService
from instorage.ai_models.completion_models.context_builder import ContextBuilder
from instorage.ai_models.embedding_models.datastore.datastore import Datastore
from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelFamily,
)
from instorage.ai_models.embedding_models.embedding_model_adapters.infinity_adapter import (
    InfinityAdapter,
)
from instorage.ai_models.embedding_models.embedding_model_adapters.text_embedding_openai import (
    OpenAIEmbeddingAdapter,
)
from instorage.ai_models.embedding_models.embedding_models_repo import (
    EmbeddingModelsRepository,
)
from instorage.ai_models.transcription_models.model_adapters.whisper import (
    OpenAISTTModelAdapter,
)
from instorage.allowed_origins.allowed_origin_repo import AllowedOriginRepository
from instorage.allowed_origins.allowed_origin_service import AllowedOriginService
from instorage.analysis.analysis_repo import AnalysisRepository
from instorage.analysis.analysis_service import AnalysisService
from instorage.assistants.api.assistant_assembler import AssistantAssembler
from instorage.assistants.assistant_factory import AssistantFactory
from instorage.assistants.assistant_repo import AssistantRepository
from instorage.assistants.assistant_runner import AssistantRunner, RunnerDelegate
from instorage.assistants.assistant_service import AssistantService
from instorage.authentication.api_key_repo import ApiKeysRepository
from instorage.authentication.auth_service import AuthService
from instorage.database.database import AsyncSession
from instorage.files.file_protocol import FileProtocol
from instorage.files.file_repo import FileRepository
from instorage.files.file_service import FileService
from instorage.files.file_size_service import FileSizeService
from instorage.files.image import ImageExtractor
from instorage.files.text import TextExtractor
from instorage.groups.group_repo import GroupRepository
from instorage.groups.group_service import GroupService
from instorage.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.info_blobs.info_blob_service import InfoBlobService
from instorage.info_blobs.text_processor import TextProcessor
from instorage.info_blobs.transcriber import Transcriber
from instorage.jobs.job_repo import JobRepository
from instorage.jobs.job_service import JobService
from instorage.jobs.task_service import TaskService
from instorage.limits.limit_service import LimitService
from instorage.main.config import get_settings
from instorage.modules.module_repo import ModuleRepository
from instorage.predefined_roles.predefined_role_service import PredefinedRolesService
from instorage.predefined_roles.predefined_roles_repo import PredefinedRolesRepository
from instorage.questions.questions_repo import QuestionRepository
from instorage.roles.roles_repo import RolesRepository
from instorage.roles.roles_service import RolesService
from instorage.services.service_repo import ServiceRepository
from instorage.services.service_runner import ServiceRunner
from instorage.services.service_service import ServiceService
from instorage.sessions.session_service import SessionService
from instorage.sessions.sessions_repo import SessionRepository
from instorage.settings.setting_service import SettingService
from instorage.settings.settings_repo import SettingsRepository
from instorage.spaces.api.space_assembler import SpaceAssembler
from instorage.spaces.space_factory import SpaceFactory
from instorage.spaces.space_repo import SpaceRepository
from instorage.spaces.space_service import SpaceService
from instorage.tenants.tenant import TenantInDB
from instorage.tenants.tenant_repo import TenantRepository
from instorage.user_groups.user_groups_repo import UserGroupsRepository
from instorage.user_groups.user_groups_service import UserGroupsService
from instorage.users.user import UserInDB
from instorage.users.user_repo import UsersRepository
from instorage.users.user_service import UserService
from instorage.websites.crawl_dependencies.crawl_runs_repo import CrawlRunRepository
from instorage.websites.website_repo import WebsiteRepository
from instorage.websites.website_service import WebsiteService
from instorage.worker.task_manager import TaskManager
from instorage.workflows.assistant_guard_runner import AssistantGuardRunner
from instorage.workflows.step_repo import StepRepository

if get_settings().using_intric_proprietary:
    from instorage_prop.crawler.crawl_repo import CrawlRepository
    from instorage_prop.crawler.crawl_service import CrawlService
    from instorage_prop.crawler.crawler import Crawler
    from instorage_prop.sysadmin.sysadmin_service import SysAdminService
    from instorage_prop.users.user_service import UserService as PropUserService
    from instorage_prop.widgets.widget_repo import WidgetRepository
    from instorage_prop.widgets.widget_service import WidgetService


class Container(containers.DeclarativeContainer):

    # Configuration
    config = providers.Configuration()

    # Objects
    session = providers.Dependency(instance_of=AsyncSession)
    user = providers.Dependency(instance_of=UserInDB)
    tenant = providers.Dependency(instance_of=TenantInDB)
    embedding_model = providers.Dependency(instance_of=EmbeddingModel)
    completion_model = providers.Dependency(instance_of=CompletionModel)

    # Factories
    space_factory = providers.Factory(SpaceFactory)
    assistant_factory = providers.Factory(AssistantFactory)

    # Assemblers
    space_assembler = providers.Factory(SpaceAssembler, user=user)
    assistant_assembler = providers.Factory(AssistantAssembler, user=user)

    # Repositories
    user_repo = providers.Factory(UsersRepository, session=session)
    settings_repo = providers.Factory(SettingsRepository, session=session)
    tenant_repo = providers.Factory(TenantRepository, session=session)
    assistant_repo = providers.Factory(
        AssistantRepository, session=session, factory=AssistantFactory
    )
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
    embedding_model_repo = providers.Factory(EmbeddingModelsRepository, session=session)
    info_blob_chunk_repo = providers.Factory(InfoBlobChunkRepo, session=session)
    service_repo = providers.Factory(ServiceRepository, session=session)
    step_repo = providers.Factory(StepRepository, session=session)
    user_groups_repo = providers.Factory(UserGroupsRepository, session=session)
    analysis_repo = providers.Factory(AnalysisRepository, session=session)
    session_repo = providers.Factory(SessionRepository, session=session)
    question_repo = providers.Factory(QuestionRepository, session=session)
    file_repo = providers.Factory(FileRepository, session=session)
    website_repo = providers.Factory(WebsiteRepository, session=session)
    crawl_run_repo = providers.Factory(CrawlRunRepository, session=session)
    space_repo = providers.Factory(
        SpaceRepository, factory=space_factory, session=session
    )
    module_repo = providers.Factory(ModuleRepository, session=session)

    # Completion model adapters
    openai_model_adapter = providers.Factory(OpenAIModelAdapter, model=completion_model)
    vllm_model_adapter = providers.Factory(VLMMModelAdapter, model=completion_model)
    claude_model_adapter = providers.Factory(ClaudeModelAdapter, model=completion_model)
    azure_model_adapter = providers.Factory(
        AzureOpenAIModelAdapter, model=completion_model
    )
    completion_model_selector = providers.Selector(
        config.completion_model,
        **{
            CompletionModelFamily.OPEN_AI.value: openai_model_adapter,
            CompletionModelFamily.VLLM.value: vllm_model_adapter,
            CompletionModelFamily.CLAUDE.value: claude_model_adapter,
            CompletionModelFamily.AZURE.value: azure_model_adapter,
        }
    )

    # Embedding model adapters
    multilingual_adapter = providers.Factory(InfinityAdapter, model=embedding_model)
    openai_embedding_adapter = providers.Factory(
        OpenAIEmbeddingAdapter, model=embedding_model
    )
    embedding_model_selector = providers.Selector(
        config.embedding_model,
        **{
            EmbeddingModelFamily.E5.value: multilingual_adapter,
            EmbeddingModelFamily.OPEN_AI.value: openai_embedding_adapter,
        }
    )

    # Speech-to-text model adapter
    openai_stt_model_adapter = providers.Factory(OpenAISTTModelAdapter)

    # Datastore
    datastore = providers.Factory(
        Datastore,
        user=user,
        embedding_model_adapter=embedding_model_selector,
        info_blob_chunk_repo=info_blob_chunk_repo,
    )
    text_extractor = providers.Factory(TextExtractor)
    image_extractor = providers.Factory(ImageExtractor)

    # Services
    ai_models_service = providers.Factory(
        AIModelsService,
        user=user,
        embedding_model_repo=embedding_model_repo,
        completion_model_repo=completion_model_repo,
        tenant_repo=tenant_repo,
    )
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
        info_blob_repo=info_blob_repo,
    )
    space_service = providers.Factory(
        SpaceService,
        user=user,
        repo=space_repo,
        factory=space_factory,
        user_repo=user_repo,
        ai_models_service=ai_models_service,
    )
    group_service = providers.Factory(
        GroupService,
        user=user,
        repo=group_repo,
        tenant_repo=tenant_repo,
        info_blob_repo=info_blob_repo,
        ai_models_service=ai_models_service,
        space_service=space_service,
    )
    quota_service = providers.Factory(
        QuotaService, user=user, info_blob_repo=info_blob_repo
    )
    job_service = providers.Factory(
        JobService,
        user=user,
        job_repo=job_repo,
    )
    file_size_service = providers.Factory(
        FileSizeService,
    )
    task_service = providers.Factory(
        TaskService,
        user=user,
        group_service=group_service,
        file_size_service=file_size_service,
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
        ai_models_service=ai_models_service,
    )
    website_service = providers.Factory(
        WebsiteService,
        user=user,
        repo=website_repo,
        task_service=task_service,
        ai_models_service=ai_models_service,
        crawl_run_repo=crawl_run_repo,
        space_service=space_service,
    )
    info_blob_service = providers.Factory(
        InfoBlobService,
        repo=info_blob_repo,
        user=user,
        quota_service=quota_service,
        website_service=website_service,
        group_service=group_service,
    )
    assistant_service = providers.Factory(
        AssistantService,
        user=user,
        repo=assistant_repo,
        auth_service=auth_service,
        service_repo=service_repo,
        step_repo=step_repo,
        ai_models_service=ai_models_service,
        group_service=group_service,
        website_service=website_service,
        space_service=space_service,
        factory=assistant_factory,
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
    settings_service = providers.Factory(
        SettingService,
        user=user,
        repo=settings_repo,
        ai_models_service=ai_models_service,
    )
    session_service = providers.Factory(
        SessionService,
        user=user,
        question_repo=question_repo,
        session_repo=session_repo,
    )
    service_service = providers.Factory(
        ServiceService,
        repo=service_repo,
        question_repo=question_repo,
        group_service=group_service,
        user=user,
        ai_models_service=ai_models_service,
        space_service=space_service,
    )
    file_protocol = providers.Factory(
        FileProtocol,
        file_size_service=file_size_service,
        text_extractor=text_extractor,
        image_extractor=image_extractor,
    )
    file_service = providers.Factory(
        FileService,
        user=user,
        repo=file_repo,
        protocol=file_protocol,
    )
    limit_service = providers.Factory(LimitService)

    # Completion
    context_builder = providers.Factory(ContextBuilder)
    completion_service = providers.Factory(
        CompletionService,
        user=user,
        user_service=user_service,
        context_builder=context_builder,
        model_adapter=completion_model_selector,
    )
    runner_delegate = providers.Factory(
        RunnerDelegate,
        info_blobs_repo=info_blob_repo,
        datastore=datastore,
    )
    assistant_runner = providers.Factory(
        AssistantRunner,
        session_service=session_service,
        completion_service=completion_service,
        runner_delegate=runner_delegate,
        file_service=file_service,
        ai_models_service=ai_models_service,
        space_service=space_service,
    )
    service_runner = providers.Factory(
        ServiceRunner,
        user=user,
        completion_service=completion_service,
        runner_delegate=runner_delegate,
        question_repo=question_repo,
        file_service=file_service,
    )
    assistant_guard_runner = providers.Factory(
        AssistantGuardRunner, session_service=session_service
    )
    analysis_service = providers.Factory(
        AnalysisService,
        user=user,
        repo=analysis_repo,
        assistant_service=assistant_service,
        session_repo=session_repo,
        question_repo=question_repo,
        completion_service=completion_service,
        space_service=space_service,
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
        extractor=text_extractor,
        datastore=datastore,
        info_blob_service=info_blob_service,
        session=session,
    )
    transcriber = providers.Factory(
        Transcriber,
        adapter=openai_stt_model_adapter,
    )

    if get_settings().using_intric_proprietary:
        # Repositories
        crawl_repo = providers.Factory(CrawlRepository, session=session)
        widget_repo = providers.Factory(WidgetRepository, session=session)

        # Services
        crawl_service = providers.Factory(
            CrawlService,
            user=user,
            repo=crawl_repo,
            task_service=task_service,
            crawl_run_repo=crawl_run_repo,
            group_service=group_service,
        )
        sysadmin_service = providers.Factory(SysAdminService)
        widget_service = providers.Factory(
            WidgetService,
            user=user,
            widget_repo=widget_repo,
            assistant_service=assistant_service,
            tenant_repo=tenant_repo,
        )
        prop_user_service = providers.Factory(
            PropUserService, user=user, user_repo=user_repo
        )

        # Worker
        crawler = providers.Factory(Crawler)
