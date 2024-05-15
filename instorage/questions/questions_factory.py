from fastapi import Depends

from instorage.database.database import AsyncSession
from instorage.questions.questions_repo import QuestionRepository
from instorage.server.dependencies.db import get_session


def get_questions_repo(session: AsyncSession = Depends(get_session)):
    return QuestionRepository(session)
