from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID


class Integration:
    def __init__(self, id: "UUID", name: str, description: str):
        self.id = id
        self.name = name
        self.description = description
