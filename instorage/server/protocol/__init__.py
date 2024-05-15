from typing import Type

from pydantic import BaseModel


def to_paginated_response(items: list):
    return {"count": len(items), "items": items}


def to_paginated_response_with_public(items: list, public_items: list):
    return {
        "count": len(items),
        "items": items,
        "public_count": len(public_items),
        "public_items": public_items,
    }


def to_uuid(object: BaseModel, type: Type[BaseModel]):
    return type(**object.model_dump(exclude={"id"}), id=object.uuid)
