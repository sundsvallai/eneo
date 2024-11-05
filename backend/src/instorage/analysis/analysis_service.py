# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from datetime import date, datetime
from uuid import UUID

from instorage.ai_models.completion_models.completion_service import CompletionService
from instorage.analysis.analysis import Counts
from instorage.analysis.analysis_prompt import SWEDISH_PROMPT
from instorage.analysis.analysis_repo import AnalysisRepository
from instorage.assistants.assistant_service import AssistantService
from instorage.main.exceptions import UnauthorizedException
from instorage.main.logging import get_logger
from instorage.questions.questions_repo import QuestionRepository
from instorage.roles.permissions import Permission, validate_permissions
from instorage.sessions.sessions_repo import SessionRepository
from instorage.spaces.space_service import SpaceService
from instorage.users.user import UserInDB

logger = get_logger(__name__)


class AnalysisService:
    def __init__(
        self,
        user: UserInDB,
        repo: AnalysisRepository,
        assistant_service: AssistantService,
        question_repo: QuestionRepository,
        session_repo: SessionRepository,
        space_service: SpaceService,
        completion_service: CompletionService = None,
    ):
        self.user = user
        self.repo = repo
        self.assistant_service = assistant_service
        self.session_repo = session_repo
        self.question_repo = question_repo
        self.completion_service = completion_service
        self.space_service = space_service

    @validate_permissions(Permission.INSIGHTS)
    async def get_tenant_counts(self):
        assistant_count = await self.repo.get_assistant_count(
            tenant_id=self.user.tenant_id
        )
        session_count = await self.repo.get_session_count(tenant_id=self.user.tenant_id)
        questions_count = await self.repo.get_question_count(
            tenant_id=self.user.tenant_id
        )

        counts = Counts(
            assistants=assistant_count,
            sessions=session_count,
            questions=questions_count,
        )

        return counts

    @validate_permissions(Permission.INSIGHTS)
    async def get_metadata_statistics(self, start_date: datetime, end_date: datetime):
        assistants = await self.assistant_service.get_tenant_assistants(
            start_date=start_date, end_date=end_date
        )
        sessions = await self.session_repo.get_by_tenant(
            self.user.tenant_id, start_date=start_date, end_date=end_date
        )
        questions = await self.question_repo.get_by_tenant(
            self.user.tenant_id, start_date=start_date, end_date=end_date
        )

        return assistants, sessions, questions

    async def _check_space_permissions(self, space_id: UUID):
        space = await self.space_service.get_space(space_id)
        if space.is_personal() and Permission.INSIGHTS not in self.user.permissions:
            raise UnauthorizedException(
                f"Need permission {Permission.INSIGHTS.value} in order to access"
            )

    async def get_questions_since(
        self,
        assistant_id: UUID,
        from_date: date,
        to_date: date,
        include_followups: bool = False,
    ):
        assistant = await self.assistant_service.get_assistant(assistant_id)
        if assistant.space_id is not None:
            await self._check_space_permissions(assistant.space_id)

        sessions = await self.repo.get_assistant_sessions_since(
            assistant_id=assistant_id,
            from_date=from_date,
            to_date=to_date,
        )

        if include_followups:
            return [question for session in sessions for question in session.questions]

        first_questions = []
        for session in sessions:
            questions = session.questions
            if questions:
                first_questions.append(questions[0])
            else:

                # Session did not contain any questions, log this as an error
                # and don't add anything to the list
                logger.error(
                    "Session was empty",
                    extra=dict(session_id=session.id),
                )

        return first_questions

    async def ask_question_on_questions(
        self,
        question: str,
        stream: bool,
        assistant_id: UUID,
        from_date: date,
        to_date: date,
        include_followup: bool = False,
    ):
        questions = await self.get_questions_since(
            assistant_id=assistant_id,
            from_date=from_date,
            to_date=to_date,
            include_followups=include_followup,
        )

        days = (to_date - from_date).days
        prompt = SWEDISH_PROMPT.format(days=days)
        questions_string = "\n".join(
            f'"""{question.question}"""' for question in questions
        )
        prompt = f"{prompt}\n\n{questions_string}"

        ai_response = await self.completion_service.get_response(
            question=question, prompt=prompt, stream=stream
        )

        return ai_response
