import json

from instorage.ai_models.completion_models.llms import get_completion_model
from instorage.groups.group import GroupPublic
from instorage.info_blobs.info_blob import InfoBlobMetadata, InfoBlobPublic
from instorage.main.logging import get_logger
from instorage.questions.question import QuestionInDB
from instorage.server import protocol
from instorage.services.service import (
    ServiceInDBWithUser,
    ServicePublicWithUser,
    ServiceRun,
)

logger = get_logger(__name__)


def from_domain_service(service: ServiceInDBWithUser):
    return ServicePublicWithUser(
        **service.model_dump(exclude={"id", "groups"}),
        id=service.uuid,
        groups=[protocol.to_uuid(group, GroupPublic) for group in service.groups]
    )


def to_question(question: QuestionInDB, service: ServiceInDBWithUser):
    try:
        output = json.loads(question.answer)
    except json.JSONDecodeError:
        logger.warning("%s is not valid JSON. Returning raw", question.answer)
        output = question.answer

    return ServiceRun(
        id=question.uuid,
        input=question.question,
        output=output,
        completion_model=get_completion_model(service.completion_model),
        references=[
            InfoBlobPublic(
                **blob.model_dump(), metadata=InfoBlobMetadata(**blob.model_dump())
            )
            for blob in question.info_blobs
        ],
    )
