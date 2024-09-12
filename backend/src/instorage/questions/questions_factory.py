from fastapi import Depends

from instorage.database.database import AsyncSession, get_session
from instorage.questions.questions_repo import QuestionRepository


def get_questions_repo(session: AsyncSession = Depends(get_session)):
    return QuestionRepository(session)
