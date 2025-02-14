from fastapi import Depends

from intric.database.database import AsyncSession, get_session_with_transaction
from intric.questions.questions_repo import QuestionRepository


def get_questions_repo(session: AsyncSession = Depends(get_session_with_transaction)):
    return QuestionRepository(session)
