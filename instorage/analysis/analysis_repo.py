# MIT License


import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.questions_table import InfoBlobReferences, Questions
from instorage.database.tables.sessions_table import Sessions
from instorage.database.tables.users_table import Users
from instorage.sessions.session import SessionInDB


class AnalysisRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_count(self, table, tenant_id: int = None):
        stmt = sa.select(sa.func.count()).select_from(table)

        if tenant_id is not None:
            if table == Questions:
                stmt = stmt.join(Sessions)

            stmt = stmt.join(Users).where(Users.tenant_id == tenant_id)

        count = await self.session.scalar(stmt)

        return count

    async def get_assistant_count(self, tenant_id: int = None):
        return await self._get_count(Assistants, tenant_id=tenant_id)

    async def get_session_count(self, tenant_id: int = None):
        return await self._get_count(Sessions, tenant_id=tenant_id)

    async def get_question_count(self, tenant_id: int = None):
        return await self._get_count(Questions, tenant_id=tenant_id)

    async def get_assistant_sessions_since(
        self, assistant_uuid: UUID, since: datetime.date
    ):
        stmt = (
            sa.select(Sessions)
            .join(
                Assistants,
                Sessions.assistant_id == Assistants.id,
            )
            .where(Assistants.uuid == assistant_uuid)
            .filter(Sessions.created_at >= since)
            .order_by(Sessions.created_at)
            .options(
                selectinload(Sessions.questions)
                .selectinload(Questions.info_blob_references)
                .selectinload(InfoBlobReferences.info_blob)
                .selectinload(InfoBlobs.group)
            )
            .options(
                selectinload(Sessions.questions).selectinload(Questions.logging_details)
            )
            .options(selectinload(Sessions.questions).selectinload(Questions.assistant))
            .options(selectinload(Sessions.assistant).selectinload(Assistants.user))
        )

        sessions = await self.session.scalars(stmt)

        return [SessionInDB.model_validate(session) for session in sessions]
