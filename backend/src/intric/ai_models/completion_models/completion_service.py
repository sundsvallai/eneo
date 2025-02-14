from __future__ import annotations

from typing import TYPE_CHECKING

from intric.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelFamily,
    CompletionModelResponse,
    ModelKwargs,
)
from intric.ai_models.completion_models.completion_model_adapters import (
    AzureOpenAIModelAdapter,
    ClaudeModelAdapter,
    OpenAIModelAdapter,
    VLMMModelAdapter,
)
from intric.ai_models.completion_models.context_builder import ContextBuilder
from intric.files.file_models import File
from intric.info_blobs.info_blob import InfoBlobChunkInDBWithScore
from intric.main.logging import get_logger
from intric.sessions.session import SessionInDB

if TYPE_CHECKING:
    from intric.main.container.container import Container

logger = get_logger(__name__)


class CompletionService:
    def __init__(
        self,
        model_adapter: OpenAIModelAdapter | ClaudeModelAdapter | VLMMModelAdapter,
        context_builder: ContextBuilder,
    ):
        self.model_adapter = model_adapter
        self.context_builder = context_builder

    async def get_response(
        self,
        text_input: str,
        model_kwargs: ModelKwargs | None = None,
        files: list[File] = [],
        prompt: str = "",
        prompt_files: list[File] = [],
        transcription_inputs: list[str] = [],
        info_blob_chunks: list[InfoBlobChunkInDBWithScore] = [],
        session: SessionInDB | None = None,
        stream: bool = False,
        extended_logging: bool = False,
        version: int = 1,
    ):
        # Make sure everything fits in the context of the model
        max_tokens = self.model_adapter.get_token_limit_of_model()

        context = self.context_builder.build_context(
            input_str=text_input,
            max_tokens=max_tokens,
            files=files,
            prompt=prompt,
            session=session,
            info_blob_chunks=info_blob_chunks,
            prompt_files=prompt_files,
            transcription_inputs=transcription_inputs,
            version=version,
        )

        if extended_logging:
            logging_details = self.model_adapter.get_logging_details(
                context=context, model_kwargs=model_kwargs
            )
        else:
            logging_details = None

        if not stream:
            completion = await self.model_adapter.get_response(
                context=context,
                model_kwargs=model_kwargs,
            )
        else:
            # Will be an async generator - not awaitable
            completion = self.model_adapter.get_response_streaming(
                context=context,
                model_kwargs=model_kwargs,
            )

        return CompletionModelResponse(
            completion=completion,
            model=self.model_adapter.model,
            extended_logging=logging_details,
            total_token_count=context.token_count,
        )


class CompletionServiceFactory:
    def __init__(self, container: Container):
        self.container = container

    def create_completion_service(self, completion_model: CompletionModel):
        match completion_model.family:
            case CompletionModelFamily.OPEN_AI:
                adapter = OpenAIModelAdapter(completion_model)
            case CompletionModelFamily.VLLM:
                adapter = VLMMModelAdapter(completion_model)
            case CompletionModelFamily.CLAUDE:
                adapter = ClaudeModelAdapter(completion_model)
            case CompletionModelFamily.AZURE:
                adapter = AzureOpenAIModelAdapter(completion_model)

        return self.container.completion_service(model_adapter=adapter)
