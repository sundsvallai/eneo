from intric.info_blobs.info_blob import InfoBlobMetadata, InfoBlobPublicNoText
from intric.logging import logging_protocol
from intric.main.models import ModelId
from intric.questions.question import Message, MessageLogging, Question, UseTools


def to_question_public(question: Question):
    tools = (
        UseTools(assistants=[ModelId(id=question.tool_assistant_id)])
        if question.tool_assistant_id
        else UseTools(assistants=[])
    )

    return Message(
        **question.model_dump(exclude={"references", "tool_assistant_id"}),
        references=[
            InfoBlobPublicNoText(
                **blob.model_dump(),
                metadata=InfoBlobMetadata(**blob.model_dump()),
            )
            for blob in question.info_blobs
        ],
        tools=tools,
    )


def to_question_logging(question: Question):
    question_public = to_question_public(question)
    return MessageLogging(
        **question_public.model_dump(),
        logging_details=logging_protocol.from_domain(question.logging_details),
    )
