from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from instorage.assistants.assistant_runner import AssistantRunner, RunnerDelegate
from instorage.info_blobs.info_blob import InfoBlobChunkInDBWithScore
from instorage.main.exceptions import BadRequestException
from tests.fixtures import TEST_UUID


@pytest.fixture(name="runner")
def assistant_runner_fixture():
    return AssistantRunner(
        assistant=MagicMock(),
        session_service=AsyncMock(),
        completion_service=AsyncMock(),
        file_service=AsyncMock(),
        runner_delegate=AsyncMock(),
        ai_models_service=AsyncMock(),
        space_service=AsyncMock(),
    )


def _create_chunk_with_score(score: float, info_blob_id: str = TEST_UUID):
    return InfoBlobChunkInDBWithScore(
        info_blob_id=info_blob_id,
        score=score,
        user_id=1,
        id=TEST_UUID,
        chunk_no=1,
        text="chunk",
        group_id=1,
        embedding=[1, 2, 3],
        tenant_id=TEST_UUID,
    )


def test_remove_duplicate_chunk_keep_highest_score_one_info_blob():
    delegate = RunnerDelegate(AsyncMock(), AsyncMock())

    chunks = [
        _create_chunk_with_score(0.9),
        _create_chunk_with_score(0.3),
        _create_chunk_with_score(0.1),
    ]

    pruned_chunks = delegate._get_info_blob_chunks_without_duplicates(chunks)

    assert pruned_chunks == [_create_chunk_with_score(0.9)]


def test_remove_duplicate_chunks_multiple_info_blobs():
    delegate = RunnerDelegate(AsyncMock(), AsyncMock())

    blob_2_id = uuid4()
    blob_3_id = uuid4()

    chunks = [
        _create_chunk_with_score(0.9),
        _create_chunk_with_score(0.7, blob_2_id),
        _create_chunk_with_score(0.3),
        _create_chunk_with_score(0.25, blob_2_id),
        _create_chunk_with_score(0.1),
        _create_chunk_with_score(0.001, blob_3_id),
    ]

    pruned_chunks = delegate._get_info_blob_chunks_without_duplicates(chunks)

    assert pruned_chunks == [
        _create_chunk_with_score(0.9),
        _create_chunk_with_score(0.7, blob_2_id),
        _create_chunk_with_score(0.001, blob_3_id),
    ]


@pytest.mark.parametrize(
    ("num_questions", "expected_answer"),
    (
        (1, "Question 0\nAnswer 0\nnext question"),
        (2, "Question 0\nAnswer 0\nQuestion 1\nAnswer 1\nnext question"),
        (0, "next question"),
    ),
)
def test_concatenate_session_and_question(num_questions: int, expected_answer: str):

    def get_questions(num_questions: int):
        questions = []
        for i in range(num_questions):
            question = MagicMock()
            question.question = f"Question {i}"
            question.answer = f"Answer {i}"
            questions.append(question)

        return questions

    questions = get_questions(num_questions)
    session = MagicMock()
    session.questions = questions

    delegate = RunnerDelegate(AsyncMock(), AsyncMock())
    concatenated_session = delegate.concatenate_conversation(session, "next question")
    assert concatenated_session == expected_answer


def test_concatenate_session_is_null():
    delegate = RunnerDelegate(AsyncMock(), AsyncMock())
    concatenated_session = delegate.concatenate_conversation(None, "next question")
    assert concatenated_session == "next question"


async def test_completion_model_disabled_in_space(runner: AssistantRunner):
    assistant = MagicMock(completion_model_id=uuid4(), space_id=uuid4())
    runner.assistant = assistant

    space = MagicMock()
    space.is_completion_model_in_space.return_value = False
    runner.space_service.get_space.return_value = space

    with pytest.raises(BadRequestException):
        await runner.run(question="hello")


async def test_group_embedding_model_disabled_in_space(runner: AssistantRunner):
    assistant = MagicMock(
        space_id=uuid4(),
        groups=[MagicMock(embedding_model_id=uuid4())],
        websites=[],
    )
    runner.assistant = assistant

    space = MagicMock()
    space.is_embedding_model_in_space.return_value = False
    runner.space_service.get_space.return_value = space

    with pytest.raises(BadRequestException):
        await runner.run(question="hello")


async def test_website_embedding_model_disabled_in_space(runner: AssistantRunner):
    assistant = MagicMock(
        space_id=uuid4(),
        websites=[MagicMock(embedding_model_id=uuid4())],
        groups=[],
    )
    runner.assistant = assistant

    space = MagicMock()
    space.is_embedding_model_in_space.return_value = False
    runner.space_service.get_space.return_value = space

    with pytest.raises(BadRequestException):
        await runner.run(question="hello")
