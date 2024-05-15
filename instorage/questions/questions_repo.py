from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.logging_table import logging_table
from instorage.database.tables.questions_table import InfoBlobReferences, Questions
from instorage.database.tables.sessions_table import Sessions
from instorage.database.tables.users_table import Users
from instorage.info_blobs.info_blob import InfoBlobChunkWithScore
from instorage.questions.question import QuestionAdd, QuestionInDB


class QuestionRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            Questions,
            QuestionInDB,
            with_options=self._get_options(),
        )
        self.session = session

    def _get_options(self):
        return [
            selectinload(Questions.info_blob_references)
            .selectinload(InfoBlobReferences.info_blob)
            .selectinload(InfoBlobs.group),
            selectinload(Questions.logging_details),
            selectinload(Questions.assistant),
            selectinload(Questions.session),
        ]

    def _add_options(self, stmt: sa.Select | sa.Insert | sa.Update):
        for option in self._get_options():
            stmt = stmt.options(option)

        return stmt

    async def _get_info_blob_record(self, id: str):
        stmt = (
            sa.select(InfoBlobs)
            .where(InfoBlobs.id == id)
            .options(selectinload(InfoBlobs.group))
        )

        return await self.session.scalar(stmt)

    async def _add_reference(self, question_id: int, chunk: InfoBlobChunkWithScore):
        stmt = (
            sa.insert(InfoBlobReferences)
            .values(
                question_id=question_id,
                info_blob_id=chunk.info_blob_old_id,
                similarity_score=chunk.score,
            )
            .returning(InfoBlobReferences)
        )

        return await self.session.scalar(stmt)

    async def _add_references(
        self, question_id: int, chunks: list[InfoBlobChunkWithScore]
    ):
        references = [await self._add_reference(question_id, chunk) for chunk in chunks]

        return references

    async def get(self, question_id: UUID):
        return await self.delegate.get_by(conditions={Questions.uuid: question_id})

    async def add(
        self, question: QuestionAdd, info_blob_chunks: list[InfoBlobChunkWithScore] = []
    ):
        stmt = (
            sa.insert(Questions)
            .values(**question.model_dump(exclude={"info_blobs", "logging_details"}))
            .returning(Questions)
        )

        stmt = self._add_options(stmt)

        question_record = await self.session.scalar(stmt)

        question_record.info_blob_references = await self._add_references(
            question_record.id, info_blob_chunks
        )

        if question.logging_details is not None:
            stmt = (
                sa.insert(logging_table)
                .values(**question.logging_details.model_dump())
                .returning(logging_table)
            )
            result = await self.session.execute(stmt)
            logging_details = result.scalar_one()
            question_record.logging_details = logging_details

        return await self.get(question_record.uuid)

    async def get_by_service(self, service_id: int):
        stmt = (
            sa.select(Questions)
            .where(Questions.service_id == service_id)
            .order_by(Questions.created_at)
        )

        return await self.delegate.get_models_from_query(stmt)

    async def get_by_tenant(
        self, tenant_id: int, start_date: datetime, end_date: datetime
    ):
        stmt = (
            sa.select(Questions)
            .where(Questions.session_id is not None)
            .join(Sessions)
            .join(Users)
            .where(Users.tenant_id == tenant_id)
            .filter(Questions.created_at >= start_date)
            .filter(Questions.created_at <= end_date)
            .order_by(Questions.created_at)
        )

        return await self.delegate.get_models_from_query(stmt)
