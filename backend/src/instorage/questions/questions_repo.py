from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.logging_table import logging_table
from instorage.database.tables.questions_table import (
    InfoBlobReferences,
    Questions,
    QuestionsFiles,
)
from instorage.database.tables.sessions_table import Sessions
from instorage.database.tables.users_table import Users
from instorage.files.file_models import File
from instorage.info_blobs.info_blob import InfoBlobChunkInDBWithScore
from instorage.questions.question import Question, QuestionAdd


class QuestionRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            Questions,
            Question,
            with_options=self._get_options(),
        )
        self.session = session

    def _get_options(self):
        return [
            selectinload(Questions.completion_model),
            selectinload(Questions.info_blob_references)
            .selectinload(InfoBlobReferences.info_blob)
            .selectinload(InfoBlobs.group),
            selectinload(Questions.logging_details),
            selectinload(Questions.assistant),
            selectinload(Questions.session),
            selectinload(Questions.files),
            selectinload(Questions.info_blob_references)
            .selectinload(InfoBlobReferences.info_blob)
            .selectinload(InfoBlobs.website),
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

    async def _add_references(
        self, question_id: int, chunks: list[InfoBlobChunkInDBWithScore]
    ):
        if not chunks:
            return []

        stmt = (
            sa.insert(InfoBlobReferences)
            .values(
                [
                    dict(
                        question_id=question_id,
                        info_blob_id=chunk.info_blob_id,
                        similarity_score=chunk.score,
                    )
                    for chunk in chunks
                ]
            )
            .returning(InfoBlobReferences)
        )

        return (await self.session.scalars(stmt)).all()

    async def _add_files(self, question_id: int, files: list[File]):
        stmt = sa.insert(QuestionsFiles).values(
            [dict(question_id=question_id, file_id=file.id) for file in files]
        )

        await self.session.execute(stmt)

    async def get(self, id: UUID):
        return await self.delegate.get(id)

    async def add(
        self,
        question: QuestionAdd,
        info_blob_chunks: list[InfoBlobChunkInDBWithScore] = [],
        files: list[File] = [],
    ):
        stmt = (
            sa.insert(Questions)
            .values(**question.model_dump(exclude={"info_blobs", "logging_details"}))
            .returning(Questions)
        )

        stmt = self._add_options(stmt)

        question_record = await self.session.scalar(stmt)

        question_record.info_blob_references = await self._add_references(
            question_id=question_record.id, chunks=info_blob_chunks
        )

        if files:
            await self._add_files(question_id=question_record.id, files=files)

        if question.logging_details is not None:
            stmt = (
                sa.insert(logging_table)
                .values(**question.logging_details.model_dump())
                .returning(logging_table)
            )
            result = await self.session.execute(stmt)
            logging_details = result.scalar_one()
            question_record.logging_details = logging_details

        return await self.get(question_record.id)

    async def get_by_service(self, service_id: int):
        stmt = (
            sa.select(Questions)
            .where(Questions.service_id == service_id)
            .order_by(Questions.created_at)
        )

        return await self.delegate.get_models_from_query(stmt)

    async def get_by_tenant(
        self, tenant_id: UUID, start_date: datetime, end_date: datetime
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
