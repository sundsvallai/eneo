import pydantic

from instorage.ai_models.completion_models.completion_model_service import (
    CompletionModelService,
)
from instorage.assistants.assistant_runner import RunnerDelegate
from instorage.main.exceptions import PydanticParseError
from instorage.main.logging import get_logger
from instorage.questions.question import QuestionAdd
from instorage.questions.questions_repo import QuestionRepository
from instorage.services.output_parsing.output_parser import OutputParserBase
from instorage.services.service import RunnerResult, ServiceInDBWithUser

logger = get_logger(__name__)


class ServiceRunner:
    def __init__(
        self,
        service: ServiceInDBWithUser,
        completion_model_service: CompletionModelService,
        output_parser: OutputParserBase,
        runner_delegate: RunnerDelegate,
        question_repo: QuestionRepository,
        prompt: str,
    ):
        self.service = service
        self.completion_model_service = completion_model_service
        self.output_parser = output_parser
        self.runner_delegate = runner_delegate
        self.question_repo = question_repo
        self.prompt = prompt

    async def run(self, input: str):
        # Get the relevant texts
        datastore_result = await self.runner_delegate.get_references(input)

        # Query the AI models
        ai_response = await self.completion_model_service.get_response(
            question=input,
            prompt=self.prompt,
            info_blobs=datastore_result.chunks,
            extended_logging=self.service.logging_enabled,
        )

        logger.debug(f"Service response: '{ai_response.completion}'")

        try:
            output = self.output_parser.parse(ai_response.completion)
        except pydantic.ValidationError as e:
            raise PydanticParseError("Error parsing output.") from e

        # Save
        question = QuestionAdd(
            question=input,
            answer=output.to_string(),
            model=ai_response.model,
            service_id=self.service.id,
            logging_details=ai_response.extended_logging,
        )
        await self.question_repo.add(
            question, info_blob_chunks=datastore_result.no_duplicate_chunks
        )

        return RunnerResult(result=output.to_value(), datastore_result=datastore_result)
