from uuid import UUID

from instorage.assistants.assistant import AssistantInDBWithUser
from instorage.info_blobs.info_blob import InfoBlobChunkWithScore
from instorage.logging.logging import LoggingDetails
from instorage.main.exceptions import NotFoundException, UnauthorizedException
from instorage.questions.question import QuestionAdd
from instorage.questions.questions_repo import QuestionRepository
from instorage.sessions.session import SessionAdd, SessionFeedback, SessionInDB
from instorage.sessions.sessions_repo import SessionRepository
from instorage.users.user import UserInDB


class SessionService:
    def __init__(
        self,
        session_repo: SessionRepository,
        question_repo: QuestionRepository,
        user: UserInDB,
    ):
        self.session_repo = session_repo
        self.question_repo = question_repo
        self.user = user

    def _check_exists_and_belongs_to_user(
        self, session: SessionInDB, assistant_id: UUID = None
    ):
        if session is None:
            raise NotFoundException("Session not found")
        if session.user_id != self.user.id:
            raise UnauthorizedException("Session belongs to other user")
        if assistant_id is not None and session.assistant.uuid != assistant_id:
            raise NotFoundException("Session belongs to another assistant")

    async def get_session_by_uuid(self, id: UUID, assistant_id: UUID = None):
        session = await self.session_repo.get(uuid=id)

        self._check_exists_and_belongs_to_user(session, assistant_id=assistant_id)

        return session

    async def get_sessions_by_assistant(self, assistant_id: UUID):
        return await self.session_repo.get_by_assistant(assistant_id, self.user.id)

    async def update_session(self, session_update):
        session = await self.session_repo.update(session_update)
        self._check_exists_and_belongs_to_user(session)
        return session

    async def delete(self, id: UUID, assistant_id: UUID = None):
        session = await self.session_repo.get(id)
        self._check_exists_and_belongs_to_user(session, assistant_id=assistant_id)
        return await self.session_repo.delete(session.id)

    async def create_session(self, name: str, assistant: AssistantInDBWithUser):
        session_add = SessionAdd(
            name=name, user_id=self.user.id, assistant_id=assistant.id
        )

        return await self.session_repo.add(session_add)

    async def add_question_to_session(
        self,
        question: str,
        answer: str,
        session: SessionInDB,
        model: str = None,
        info_blob_chunks: InfoBlobChunkWithScore = [],
        logging_details: LoggingDetails = None,
    ):
        question_add = QuestionAdd(
            question=question,
            answer=answer,
            model=model,
            session_id=session.id,
            logging_details=logging_details,
        )

        await self.question_repo.add(question_add, info_blob_chunks=info_blob_chunks)

    async def leave_feedback(
        self, session_id: UUID, assistant_id: UUID, feedback: SessionFeedback
    ):
        session = await self.session_repo.get(uuid=session_id)
        self._check_exists_and_belongs_to_user(session, assistant_id=assistant_id)
        return await self.session_repo.add_feedback(feedback=feedback, id=session.id)
