# MIT License

from pathlib import Path

import openai
from openai import AsyncOpenAI
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from intric.files.audio import AudioFile
from intric.main.config import get_settings
from intric.main.exceptions import BadRequestException, OpenAIException
from intric.main.logging import get_logger

logger = get_logger(__name__)


class OpenAISTTModelAdapter:
    def __init__(
        self,
        client: AsyncOpenAI = AsyncOpenAI(
            api_key=get_settings().openai_api_key,
            base_url=get_settings().whisper_model_url,
        ),
    ):
        self.client = client

    async def get_text_from_file(self, audio_file: AudioFile):
        text = ""
        five_minutes = 60 * 5
        async with audio_file.asplit_file(seconds=five_minutes) as files:
            for path in files:
                block_text = await self._get_text_from_file(path)
                text = f"{text}{block_text}"

        return text

    @retry(
        wait=wait_random_exponential(min=1, max=20),
        stop=stop_after_attempt(3),
        retry=retry_if_not_exception_type(BadRequestException),
        reraise=True,
    )
    async def _get_text_from_file(self, file: Path):
        try:
            transcription = await self.client.audio.transcriptions.create(
                model=get_settings().whisper_model_name,
                file=file,
            )
        except openai.BadRequestError as e:
            logger.exception("Bad request error:")
            raise BadRequestException("Invalid input") from e
        except openai.RateLimitError as e:
            logger.exception("Rate limit error:")
            raise OpenAIException("OpenAI Ratelimit exception") from e
        except Exception as e:
            logger.exception("Unknown OpenAI exception:")
            raise OpenAIException("Unknown OpenAI exception") from e

        return transcription.text
