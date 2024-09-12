from instorage.info_blobs.info_blob import InfoBlobMetadata, InfoBlobPublicNoText
from instorage.logging import logging_protocol
from instorage.questions.question import Message, MessageLogging, Question


def to_question_public(question: Question):
    return Message(
        **question.model_dump(exclude={"references"}),
        references=[
            InfoBlobPublicNoText(
                **blob.model_dump(),
                metadata=InfoBlobMetadata(**blob.model_dump()),
            )
            for blob in question.info_blobs
        ],
    )


def to_question_logging(question: Question):
    question_public = to_question_public(question)
    return MessageLogging(
        **question_public.model_dump(),
        logging_details=logging_protocol.from_domain(question.logging_details),
    )
