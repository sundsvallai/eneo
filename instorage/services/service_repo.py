from uuid import UUID

from instorage.assistants.base.agent_repos import AgentBaseRepository
from instorage.database.tables.service_table import Services
from instorage.services.service import ServiceInDBWithUser, ServiceUpsert


class ServiceRepository:
    def __init__(self, db):
        self._db = db
        self._agent_delegate = AgentBaseRepository(db, Services, ServiceInDBWithUser)

    async def add(self, service: ServiceUpsert):
        return await self._agent_delegate.add(service)

    async def get_by_uuid(self, uuid: UUID, user_id: int = None):
        return await self._agent_delegate.get_by_uuid(uuid, user_id)

    async def get_by_user(self, user_id: int, search_query: str = None):
        return await self._agent_delegate.get_by_user(user_id, search_query)

    async def get_for_user(self, user_id: int, search_query: str = None):
        return await self._agent_delegate.get_for_user(user_id, search_query)

    async def update(self, service: ServiceUpsert):
        return await self._agent_delegate.update(service)

    async def delete(self, uuid: UUID, user_id: int):
        return await self._agent_delegate.delete(uuid, user_id)
