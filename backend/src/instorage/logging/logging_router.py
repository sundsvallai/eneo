# Copyright (c) 2023 Sundsvalls Kommun
#
# Licensed under the MIT License.

from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.authentication.auth_dependencies import get_current_active_user
from instorage.main.exceptions import BadRequestException
from instorage.questions.question import MessageLogging
from instorage.questions.question_protocol import to_question_logging
from instorage.questions.questions_factory import get_questions_repo
from instorage.questions.questions_repo import QuestionRepository

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/{message_id}/", response_model=MessageLogging)
async def get_logging_details(
    message_id: UUID, question_repo: QuestionRepository = Depends(get_questions_repo)
):
    question = await question_repo.get(message_id)

    if question.logging_details is None:
        raise BadRequestException("Question was not logged.")

    return to_question_logging(question)
