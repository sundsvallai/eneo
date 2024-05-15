# MIT License

from fastapi import Depends

from instorage.ai_models.completion_models.completion_model_service import (
    CompletionModelServiceFactory,
)
from instorage.ai_models.completion_models.llms import get_completion_model
from instorage.analysis.analysis import AskAnalysis
from instorage.analysis.analysis_repo import AnalysisRepository
from instorage.analysis.analysis_service import AnalysisService
from instorage.assistants.assistant_repo import AssistantRepository
from instorage.authentication import auth_dependencies
from instorage.main.container import Container
from instorage.questions.questions_repo import QuestionRepository
from instorage.server.dependencies.container import get_container
from instorage.server.dependencies.db import get_repository
from instorage.sessions.sessions_repo import SessionRepository
from instorage.users.user import UserInDB
from instorage.users.user_factory import get_user_service
from instorage.users.user_service import UserService


def get_analysis_service(container: Container = Depends(get_container(with_user=True))):
    return container.analysis_service()


async def get_analysis_service_with_completion_model_service(
    ask_analysis: AskAnalysis,
    user: UserInDB = Depends(auth_dependencies.get_current_active_user),
    user_service: UserService = Depends(get_user_service),
    repo: AnalysisRepository = Depends(get_repository(AnalysisRepository)),
    assistant_repo: AssistantRepository = Depends(get_repository(AssistantRepository)),
    session_repo: SessionRepository = Depends(get_repository(SessionRepository)),
    question_repo: QuestionRepository = Depends(get_repository(QuestionRepository)),
):
    # Get completion model service
    completion_model = get_completion_model(ask_analysis.completion_model)
    completion_model_service = await CompletionModelServiceFactory.create(
        completion_model,
        {},
        user_service,
        user,
    )

    return AnalysisService(
        user=user,
        repo=repo,
        assistant_repo=assistant_repo,
        completion_model_service=completion_model_service,
        question_repo=question_repo,
        session_repo=session_repo,
    )
