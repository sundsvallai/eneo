import openai
from openai import AsyncOpenAI
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from instorage.main.exceptions import BadRequestException, OpenAIException
from instorage.main.logging import get_logger

logger = get_logger(__name__)


@retry(
    wait=wait_random_exponential(min=1, max=20),
    stop=stop_after_attempt(3),
    retry=retry_if_not_exception_type(BadRequestException),
    reraise=True,
)
async def get_response(
    client: AsyncOpenAI, model_name: str, messages: list, model_kwargs: dict
):
    try:
        response = await client.chat.completions.create(
            model=model_name, messages=messages, **model_kwargs
        )
        choices = response.choices  # type: ignore
        completion = choices[0].message.content.strip()
        return completion
    except openai.BadRequestError as exc:
        raise BadRequestException("Invalid model kwargs") from exc
    except openai.RateLimitError as exc:
        logger.exception("Rate limit error:")
        raise OpenAIException("Rate limit exceeded") from exc
    except Exception as exc:
        logger.exception("Unknown error:")
        raise OpenAIException("Unknown Open AI exception") from exc


@retry(
    wait=wait_random_exponential(min=1, max=20),
    stop=stop_after_attempt(3),
    retry=retry_if_not_exception_type(BadRequestException),
    reraise=True,
)
async def get_response_streaming(
    client: AsyncOpenAI, model_name: str, messages: list, model_kwargs: dict
):
    try:
        stream = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True,
            **model_kwargs,
        )

        async for chunk in stream:
            if len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content

    except openai.BadRequestError as exc:
        raise BadRequestException("Invalid model kwargs") from exc
    except openai.RateLimitError as exc:
        logger.exception("Rate limit error:")
        raise OpenAIException("Rate limit exceeded") from exc
    except Exception as exc:
        logger.exception("Unknown error:")
        raise OpenAIException("Unknown Open AI exception") from exc
