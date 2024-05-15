from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from instorage.authentication.auth_dependencies import get_current_active_user
from instorage.questions import questions_factory
from instorage.questions.questions_repo import QuestionRepository
from instorage.server.dependencies.db import get_session
from instorage.sessions.session_service import SessionService
from instorage.sessions.sessions_repo import SessionRepository
from instorage.users.user import UserInDB


def get_session_repo(session: AsyncSession = Depends(get_session)):
    return SessionRepository(session)


def get_session_service(get_user: Callable = get_current_active_user):
    def _get_session_service(
        user: UserInDB = Depends(get_user),
        session_repo: SessionRepository = Depends(get_session_repo),
        question_repo: QuestionRepository = Depends(
            questions_factory.get_questions_repo
        ),
    ):
        return SessionService(
            session_repo=session_repo, question_repo=question_repo, user=user
        )

    return _get_session_service
