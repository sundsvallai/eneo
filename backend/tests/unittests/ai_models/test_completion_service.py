from unittest.mock import AsyncMock, MagicMock

import pytest

from instorage.ai_models.completion_models.completion_model import Context
from instorage.ai_models.completion_models.completion_service import CompletionService
from instorage.main.exceptions import QueryException


def test_get_error_on_too_long_question():
    service = CompletionService(AsyncMock(), AsyncMock(), MagicMock(), MagicMock())
    input_str = "This is a loooooong query, longer than 5 tokens"
    service.context_builder.build_context.return_value = Context(
        input=input_str, prompt=""
    )

    with pytest.raises(QueryException):
        service.get_context(input_str=input_str, max_tokens=5)


def test_get_error_on_too_long_question_and_prompt():
    service = CompletionService(AsyncMock(), AsyncMock(), MagicMock(), MagicMock())
    input_str = "Short query"
    prompt_str = "This is a super long prompt string"
    service.context_builder.build_context.return_value = Context(
        input=input_str, prompt=prompt_str
    )

    with pytest.raises(QueryException):
        service.get_context(input_str=input_str, prompt=prompt_str, max_tokens=7)


@pytest.mark.parametrize(
    ["max_tokens", "expected_result", "start_count"],
    [
        (2, [1], 0),
        (3, [2, 1], 0),
        (9, [3, 2, 1], 0),
        (11, [4, 3, 2, 1], 0),
        (11, [3, 2, 1], 2),
        (100, [7, 6, 5, 4, 3, 2, 1], 0),
    ],
)
async def test_get_number_of_questions(max_tokens, expected_result, start_count):
    service = CompletionService(AsyncMock(), AsyncMock(), MagicMock(), MagicMock())

    question_counts = [7, 6, 5, 4, 3, 2, 1]
    num_questions = service.get_number_of_questions(
        max_tokens, question_counts, start_count
    )

    assert question_counts[-num_questions:] == expected_result
