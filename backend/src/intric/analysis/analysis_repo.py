# MIT License


import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from intric.database.tables.assistant_table import Assistants
from intric.database.tables.group_chats_table import GroupChatsTable
from intric.database.tables.info_blobs_table import InfoBlobs
from intric.database.tables.questions_table import (
    InfoBlobReferences,
    Questions,
    QuestionsFiles,
)
from intric.database.tables.sessions_table import Sessions
from intric.database.tables.users_table import Users
from intric.sessions.session import SessionInDB


class AnalysisRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_count(self, table, tenant_id: UUID = None):
        stmt = sa.select(sa.func.count()).select_from(table)

        if tenant_id is not None:
            if table == Questions:
                stmt = stmt.join(Sessions)

            stmt = stmt.join(Users).where(Users.tenant_id == tenant_id)

        count = await self.session.scalar(stmt)

        return count

    async def get_assistant_count(self, tenant_id: UUID = None):
        return await self._get_count(Assistants, tenant_id=tenant_id)

    async def get_group_chat_count(self, tenant_id: UUID = None):
        return await self._get_count(table=GroupChatsTable, tenant_id=tenant_id)

    async def get_session_count(self, tenant_id: UUID = None):
        return await self._get_count(Sessions, tenant_id=tenant_id)

    async def get_question_count(self, tenant_id: UUID = None):
        return await self._get_count(Questions, tenant_id=tenant_id)

    async def get_assistant_sessions_since(
        self,
        assistant_id: UUID,
        from_date: datetime = None,
        to_date: datetime = None,
    ):
        stmt = (
            sa.select(Sessions)
            .join(
                Assistants,
                Sessions.assistant_id == Assistants.id,
            )
            .where(Assistants.id == assistant_id)
        )

        if from_date is not None:
            stmt = stmt.where(Sessions.created_at >= from_date)

        if to_date is not None:
            stmt = stmt.where(Sessions.created_at <= to_date)

        stmt = (
            stmt.order_by(Sessions.created_at)
            .options(
                selectinload(Sessions.questions)
                .selectinload(Questions.info_blob_references)
                .selectinload(InfoBlobReferences.info_blob)
                .selectinload(InfoBlobs.group)
            )
            .options(
                selectinload(Sessions.questions)
                .selectinload(Questions.info_blob_references)
                .selectinload(InfoBlobReferences.info_blob)
                .selectinload(InfoBlobs.website)
            )
            .options(selectinload(Sessions.questions).selectinload(Questions.logging_details))
            .options(selectinload(Sessions.questions).selectinload(Questions.assistant))
            .options(selectinload(Sessions.questions).selectinload(Questions.completion_model))
            .options(
                selectinload(Sessions.questions)
                .selectinload(Questions.questions_files)
                .selectinload(QuestionsFiles.file)
            )
            .options(selectinload(Sessions.questions).selectinload(Questions.completion_model))
            .options(selectinload(Sessions.assistant).selectinload(Assistants.user))
            .options(
                selectinload(Sessions.questions).selectinload(Questions.web_search_results),
            )
        )

        sessions = await self.session.scalars(stmt)
        return [SessionInDB.model_validate(session) for session in sessions]

    async def get_group_chat_sessions_since(
        self,
        group_chat_id: UUID,
        from_date: datetime = None,
        to_date: datetime = None,
    ):
        stmt = sa.select(Sessions).where(Sessions.group_chat_id == group_chat_id)

        if from_date is not None:
            stmt = stmt.where(Sessions.created_at >= from_date)

        if to_date is not None:
            stmt = stmt.where(Sessions.created_at <= to_date)

        stmt = (
            stmt.order_by(Sessions.created_at)
            .options(
                selectinload(Sessions.questions)
                .selectinload(Questions.info_blob_references)
                .selectinload(InfoBlobReferences.info_blob)
                .selectinload(InfoBlobs.group)
            )
            .options(
                selectinload(Sessions.questions)
                .selectinload(Questions.info_blob_references)
                .selectinload(InfoBlobReferences.info_blob)
                .selectinload(InfoBlobs.website)
            )
            .options(selectinload(Sessions.questions).selectinload(Questions.logging_details))
            .options(selectinload(Sessions.questions).selectinload(Questions.assistant))
            .options(selectinload(Sessions.questions).selectinload(Questions.completion_model))
            .options(
                selectinload(Sessions.questions)
                .selectinload(Questions.questions_files)
                .selectinload(QuestionsFiles.file)
            )
            .options(selectinload(Sessions.group_chat))
            .options(
                selectinload(Sessions.questions).selectinload(Questions.web_search_results),
            )
        )

        sessions = await self.session.scalars(stmt)

        return [SessionInDB.model_validate(session) for session in sessions]
