from datetime import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.questions_table import InfoBlobReferences, Questions
from instorage.database.tables.sessions_table import Sessions
from instorage.database.tables.users_table import Users
from instorage.sessions.session import (
    SessionAdd,
    SessionFeedback,
    SessionInDB,
    SessionUpdate,
)


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session, Sessions, SessionInDB, with_options=self._options()
        )
        self.session = session

    @staticmethod
    def _options():
        return [
            selectinload(Sessions.questions)
            .selectinload(Questions.info_blob_references)
            .selectinload(InfoBlobReferences.info_blob)
            .selectinload(InfoBlobs.group),
            selectinload(Sessions.questions).selectinload(Questions.logging_details),
            selectinload(Sessions.questions).selectinload(Questions.assistant),
            selectinload(Sessions.assistant).selectinload(Assistants.user),
        ]

    def _add_options(self, stmt: sa.Select | sa.Insert | sa.Update):
        for option in self._options():
            stmt = stmt.options(option)

        return stmt

    async def add(self, session: SessionAdd) -> SessionInDB:
        return await self.delegate.add(session)

    async def update(self, session: SessionUpdate) -> SessionInDB:
        return await self.delegate.update(session)

    async def add_feedback(self, feedback: SessionFeedback, id: int):
        stmt = (
            sa.Update(Sessions)
            .values(feedback_value=feedback.value, feedback_text=feedback.text)
            .where(Sessions.id == id)
            .returning(Sessions)
        )

        stmt_with_options = self._add_options(stmt)
        session = await self.session.scalar(stmt_with_options)

        return SessionInDB.model_validate(session)

    async def get(
        self, uuid: Optional[UUID] = None, user_id: int = None
    ) -> SessionInDB:
        if uuid is None and user_id is None:
            raise ValueError("One of id and user_id is required")

        if uuid is not None:
            return await self.delegate.get_by(conditions={Sessions.uuid: uuid})

        return await self.delegate.filter_by(conditions={Sessions.user_id: user_id})

    async def get_by_assistant(self, assistant_id: int, user_id: int = None):
        query = (
            sa.select(Sessions)
            .where(Sessions.assistant_id == assistant_id)
            .order_by(Sessions.created_at)
        )

        if user_id is not None:
            query = query.where(Sessions.user_id == user_id)

        return await self.delegate.get_models_from_query(query)

    async def get_by_tenant(
        self, tenant_id: int, start_date: datetime = None, end_date: datetime = None
    ):
        query = sa.select(Sessions).join(Users).where(Users.tenant_id == tenant_id)

        if start_date is not None:
            query = query.filter(Sessions.created_at >= start_date)

        if end_date is not None:
            query = query.filter(Sessions.created_at <= end_date)

        return await self.delegate.get_models_from_query(query)

    async def delete(self, id: int) -> SessionInDB:
        return await self.delegate.delete(id)
