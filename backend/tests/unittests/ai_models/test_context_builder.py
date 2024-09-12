from unittest.mock import MagicMock
from uuid import uuid4

from instorage.ai_models.completion_models.completion_model import Context, Message
from instorage.ai_models.completion_models.context_builder import ContextBuilder
from instorage.ai_models.completion_models.guardrails import (
    FAIRNESS_GUARD,
    HALLUCINATION_GUARD,
)
from instorage.files.file_models import File, FileType

QUESTION = "I have a question"


def test_context_builder_basic_context():
    builder = ContextBuilder()

    context = builder.build_context(input=QUESTION)
    expected_context = Context(input=QUESTION)

    assert context == expected_context


def test_context_with_fairness_guard():
    builder = ContextBuilder()

    context = builder.build_context(input=QUESTION, fairness_guard=True)
    expected_context = Context(input=QUESTION, prompt=FAIRNESS_GUARD)

    assert context == expected_context


def test_context_with_fairness_guard_and_hallucination_guard():
    builder = ContextBuilder()

    context = builder.build_context(
        input=QUESTION, fairness_guard=True, hallucination_guard=True
    )
    expected_context = Context(
        input=QUESTION, prompt=f"{FAIRNESS_GUARD}\n\n{HALLUCINATION_GUARD}"
    )

    assert context == expected_context


def test_context_with_info_blobs():
    builder = ContextBuilder()

    info_blob_chunks = [
        MagicMock(text=f"information about blob number {i}") for i in range(3)
    ]

    expected_background_info = """\"\"\"information about blob number 0\"\"\"
\"\"\"information about blob number 1\"\"\"
\"\"\"information about blob number 2\"\"\""""

    context = builder.build_context(input=QUESTION, info_blob_chunks=info_blob_chunks)
    expected_context = Context(input=QUESTION, prompt=expected_background_info)

    assert context == expected_context


def test_context_with_info_blobs_and_guards():
    builder = ContextBuilder()

    info_blob_chunks = [
        MagicMock(text=f"information about blob number {i}") for i in range(3)
    ]

    expected_background_info = """\"\"\"information about blob number 0\"\"\"
\"\"\"information about blob number 1\"\"\"
\"\"\"information about blob number 2\"\"\""""

    context = builder.build_context(
        input=QUESTION,
        info_blob_chunks=info_blob_chunks,
        fairness_guard=True,
        hallucination_guard=True,
    )
    expected_context = Context(
        input=QUESTION,
        prompt=f"{FAIRNESS_GUARD}\n\n{HALLUCINATION_GUARD}\n\n{expected_background_info}",
    )

    assert context == expected_context


def test_context_with_files():
    builder = ContextBuilder()

    file = MagicMock(
        text="This is the text from the file",
        file_type=FileType.TEXT,
    )
    file.name = "test_file.pdf"

    context = builder.build_context(input=QUESTION, files=[file])

    expected_input = f"""Below are files uploaded by the user. You should act like you can see the files themselves:

{{"filename": "{file.name}", "text": "{file.text}"}}

{QUESTION}"""  # noqa
    expected_context = Context(input=expected_input)

    assert context == expected_context


def test_context_with_messages():
    builder = ContextBuilder()

    file = File(
        id=uuid4(),
        text="This is the text from the file",
        name="test_file.pdf",
        checksum="",
        size=0,
        tenant_id=uuid4(),
        user_id=uuid4(),
        file_type=FileType.TEXT,
    )

    session = MagicMock(
        questions=[
            MagicMock(
                question="Question 1",
                answer="Answer 1",
                files=[],
            ),
            MagicMock(
                question="Question 2 with file",
                answer="Answer 2",
                files=[file],
            ),
        ]
    )

    context = builder.build_context(input=QUESTION, session=session)

    expected_question_2 = f"""Below are files uploaded by the user. You should act like you can see the files themselves:

{{"filename": "{file.name}", "text": "{file.text}"}}

Question 2 with file"""  # noqa
    expected_messages = [
        Message(question="Question 1", answer="Answer 1"),
        Message(question=expected_question_2, answer="Answer 2"),
    ]

    expected_context = Context(input=QUESTION, messages=expected_messages)

    assert expected_context == context


def test_context_with_images():
    builder = ContextBuilder()

    image = File(
        id=uuid4(),
        image="data",
        name="test_file.png",
        checksum="",
        size=0,
        tenant_id=uuid4(),
        user_id=uuid4(),
        file_type=FileType.IMAGE,
    )

    context = builder.build_context(input=QUESTION, files=[image])

    expected_context = Context(input=QUESTION, images=[image])

    assert context == expected_context


def test_context_with_messages_and_images():
    builder = ContextBuilder()

    image = File(
        id=uuid4(),
        name="test_file.png",
        image="data",
        checksum="",
        size=0,
        tenant_id=uuid4(),
        user_id=uuid4(),
        file_type=FileType.IMAGE,
    )

    session = MagicMock(
        questions=[
            MagicMock(
                question="Question 1",
                answer="Answer 1",
                files=[],
            ),
            MagicMock(
                question="Question 2 with image",
                answer="Answer 2",
                files=[image],
            ),
        ]
    )

    context = builder.build_context(input=QUESTION, session=session)

    expected_messages = [
        Message(question="Question 1", answer="Answer 1"),
        Message(question="Question 2 with image", answer="Answer 2", images=[image]),
    ]

    expected_context = Context(input=QUESTION, messages=expected_messages)

    assert expected_context == context
