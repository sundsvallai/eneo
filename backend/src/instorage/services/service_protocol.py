import json

from instorage.info_blobs.info_blob import InfoBlobMetadata, InfoBlobPublic
from instorage.main.logging import get_logger
from instorage.questions.question import Question
from instorage.services.service import Service, ServicePublicWithUser, ServiceRun

logger = get_logger(__name__)


def from_domain_service(service: Service):
    return ServicePublicWithUser(**service.model_dump())


def to_question(question: Question, service: Service):
    try:
        output = json.loads(question.answer)
    except json.JSONDecodeError:
        logger.warning("%s is not valid JSON. Returning raw", question.answer)
        output = question.answer

    return ServiceRun(
        id=question.id,
        input=question.question,
        output=output,
        completion_model=service.completion_model,
        references=[
            InfoBlobPublic(
                **blob.model_dump(), metadata=InfoBlobMetadata(**blob.model_dump())
            )
            for blob in question.info_blobs
        ],
    )
