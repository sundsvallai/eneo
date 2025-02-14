from pydantic import BaseModel

from intric.main.models import GeneralError


def streaming_response(model: BaseModel, response_codes: list[int] = None):
    streaming = {
        200: {
            "content": {
                "text/event-stream": {
                    "schema": model.model_json_schema(
                        ref_template="#/components/schemas/{model}"
                    )
                }
            }
        }
    }

    if response_codes is not None:
        codes = get_responses(response_codes)
        streaming.update(codes)

    return streaming


def get_responses(response_codes: list[int]):
    return {code: {"model": GeneralError} for code in response_codes}
