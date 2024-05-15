from instorage.ai_models.completion_models.llms import FROM_DOMAIN, get_completion_model
from instorage.info_blobs.info_blob import InfoBlobMetadata, InfoBlobPublicNoText
from instorage.logging import logging_protocol
from instorage.questions.question import Message, MessageLogging, QuestionInDB


def to_question_public(question: QuestionInDB):
    if question.model is not None:
        model = get_completion_model(FROM_DOMAIN[question.model])
    else:
        model = None

    return Message(
        **question.model_dump(exclude={"id", "uuid", "completion_model", "references"}),
        id=question.uuid,
        completion_model=model,
        references=[
            InfoBlobPublicNoText(
                **blob.model_dump(exclude={"group_id"}),
                group_id=blob.group.uuid,
                metadata=InfoBlobMetadata(**blob.model_dump()),
            )
            for blob in question.info_blobs
        ],
    )


def to_question_logging(question: QuestionInDB):
    question_public = to_question_public(question)
    return MessageLogging(
        **question_public.model_dump(),
        logging_details=logging_protocol.from_domain(question.logging_details),
    )
