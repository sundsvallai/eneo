# MIT license

import anthropic
from anthropic import AsyncAnthropic
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from instorage.main.exceptions import BadRequestException, ClaudeException
from instorage.main.logging import get_logger

logger = get_logger(__name__)


@retry(
    wait=wait_random_exponential(min=1, max=20),
    stop=stop_after_attempt(3),
    retry=retry_if_not_exception_type(BadRequestException),
    reraise=True,
)
async def get_response(
    client: AsyncAnthropic,
    model_name: str,
    prompt: str,
    messages: list,
    model_kwargs: dict,
    max_tokens: int,
):
    try:
        message = await client.messages.create(
            max_tokens=max_tokens,
            system=prompt,
            messages=messages,
            model=model_name,
            **model_kwargs,
        )
        return message.content[0].text
    except anthropic.APIConnectionError as exc:
        logger.exception("Connection error:")
        raise ClaudeException("The server could not be reached") from exc
    except anthropic.BadRequestError as exc:
        raise BadRequestException("Invalid model kwargs") from exc
    except anthropic.RateLimitError as exc:
        logger.exception("Rate limit error:")
        raise ClaudeException("Rate limit exceeded") from exc
    except Exception as exc:
        logger.exception("Unknown error:")
        raise ClaudeException("Unknown Claude AI exception") from exc


@retry(
    wait=wait_random_exponential(min=1, max=20),
    stop=stop_after_attempt(3),
    retry=retry_if_not_exception_type(BadRequestException),
    reraise=True,
)
async def get_response_streaming(
    client: AsyncAnthropic,
    model_name: str,
    prompt: str,
    messages: list,
    model_kwargs: dict,
    max_tokens: int,
):
    try:
        stream = await client.messages.create(
            max_tokens=max_tokens,
            system=prompt,
            messages=messages,
            model=model_name,
            stream=True,
            **model_kwargs,
        )

        async for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text

    except anthropic.APIConnectionError as exc:
        logger.exception("Connection error:")
        raise ClaudeException("The server could not be reached") from exc
    except anthropic.BadRequestError as exc:
        raise BadRequestException("Invalid model kwargs") from exc
    except anthropic.RateLimitError as exc:
        logger.exception("Rate limit error:")
        raise ClaudeException("Rate limit exceeded") from exc
    except Exception as exc:
        logger.exception("Unknown error:")
        raise ClaudeException("Unknown Claude AI exception") from exc
