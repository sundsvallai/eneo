from datetime import datetime, timedelta, timezone

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from intric.database.tables.app_table import AppRuns, Apps
from intric.database.tables.assistant_table import Assistants
from intric.database.tables.questions_table import Questions
from intric.database.tables.sessions_table import Sessions


class DataRetentionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete_old_questions(self):
        subquery = (
            sa.select(Questions.id)
            .join(Assistants, Questions.assistant_id == Assistants.id)
            .where(
                sa.and_(
                    Assistants.data_retention_days.isnot(None),
                    Questions.created_at
                    < sa.func.now() - Assistants.data_retention_days * text("INTERVAL '1 day'"),
                )
            )
        )

        query = sa.delete(Questions).where(Questions.id.in_(subquery))
        await self.session.execute(query)

    async def delete_old_app_runs(self):
        subquery = (
            sa.select(AppRuns.id)
            .join(Apps, AppRuns.app_id == Apps.id)
            .where(
                sa.and_(
                    Apps.data_retention_days.isnot(None),
                    AppRuns.created_at
                    < sa.func.now() - Apps.data_retention_days * text("INTERVAL '1 day'"),
                )
            )
        )

        query = sa.delete(AppRuns).where(AppRuns.id.in_(subquery))
        await self.session.execute(query)

    async def delete_old_sessions(self):
        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)

        subquery = (
            sa.select(Sessions.id)
            .outerjoin(Questions, Sessions.id == Questions.session_id)
            .where(sa.and_(Sessions.created_at < one_day_ago, Questions.id.is_(None)))
        )

        query = sa.delete(Sessions).where(Sessions.id.in_(subquery))
        await self.session.execute(query)
