import pydantic

from instorage.ai_models.completion_models.completion_service import (
    CompletionService,
    count_tokens,
)
from instorage.assistants.assistant_runner import RunnerDelegate
from instorage.files.file_service import FileService
from instorage.main.exceptions import PydanticParseError
from instorage.main.logging import get_logger
from instorage.main.models import ModelId
from instorage.questions.question import QuestionAdd
from instorage.questions.questions_repo import QuestionRepository
from instorage.services.output_parsing.output_parser import OutputParserBase
from instorage.services.service import RunnerResult, Service
from instorage.users.user import UserInDB

logger = get_logger(__name__)


class ServiceRunner:
    def __init__(
        self,
        user: UserInDB,
        service: Service,
        completion_service: CompletionService,
        file_service: FileService,
        output_parser: OutputParserBase,
        runner_delegate: RunnerDelegate,
        question_repo: QuestionRepository,
        prompt: str,
    ):
        self.user = user
        self.service = service
        self.completion_service = completion_service
        self.output_parser = output_parser
        self.runner_delegate = runner_delegate
        self.question_repo = question_repo
        self.prompt = prompt
        self.file_service = file_service

    async def run(
        self,
        input: str,
        file_ids: list[ModelId] = [],
    ):
        # Get the relevant texts
        datastore_result = await self.runner_delegate.get_references(
            input, self.service.groups
        )

        files = await self.file_service.get_files_by_ids(file_ids)

        # Query the AI models
        ai_response = await self.completion_service.get_response(
            question=input,
            files=files,
            prompt=self.prompt,
            info_blob_chunks=datastore_result.chunks,
            model_kwargs=self.service.completion_model_kwargs,
        )

        logger.debug(f"Service response: '{ai_response.completion}'")

        try:
            output = self.output_parser.parse(ai_response.completion)
        except pydantic.ValidationError as e:
            raise PydanticParseError("Error parsing output.") from e

        # Count tokens
        answer = output.to_string()
        num_tokens_answer = count_tokens(answer)

        # Save
        question = QuestionAdd(
            tenant_id=self.user.tenant_id,
            question=input,
            answer=answer,
            num_tokens_question=ai_response.total_token_count,
            num_tokens_answer=num_tokens_answer,
            completion_model_id=self.service.completion_model.id,
            service_id=self.service.id,
        )
        await self.question_repo.add(
            question,
            info_blob_chunks=datastore_result.no_duplicate_chunks,
            files=files,
        )

        return RunnerResult(result=output.to_value(), datastore_result=datastore_result)
