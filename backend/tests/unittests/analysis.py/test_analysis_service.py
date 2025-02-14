from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from intric.analysis.analysis_service import AnalysisService
from intric.main.exceptions import UnauthorizedException
from intric.roles.permissions import Permission
from tests.fixtures import TEST_UUID


@pytest.fixture(name="user")
def user():
    return MagicMock(tenant_id=TEST_UUID)


@pytest.fixture(name="service")
def analysis_service(user):
    return AnalysisService(
        user=user,
        repo=AsyncMock(),
        assistant_service=AsyncMock(),
        question_repo=AsyncMock(),
        session_repo=AsyncMock(),
        space_service=AsyncMock(),
    )


async def test_ask_question_not_in_space(service: AnalysisService):
    service.assistant_service.get_assistant.return_value = (
        AsyncMock(space_id=None, user=service.user),
        MagicMock(),
    )

    from_date = date.today()
    to_date = from_date
    await service.ask_question_on_questions(
        question="Test",
        stream=False,
        assistant_id=uuid4(),
        from_date=from_date,
        to_date=to_date,
    )


async def test_ask_question_personal_space_no_access(service: AnalysisService):
    service.space_service.get_space.return_value = MagicMock(user_id=uuid4())
    service.assistant_service.get_assistant.return_value = (
        MagicMock(space_id=uuid4(), user=service.user),
        MagicMock(),
    )
    with pytest.raises(UnauthorizedException):
        from_date = date.today()
        to_date = from_date
        await service.ask_question_on_questions(
            question="Test",
            stream=False,
            assistant_id=uuid4(),
            from_date=from_date,
            to_date=to_date,
        )


async def test_ask_question_personal_space_with_access(service: AnalysisService):
    user = MagicMock(tenant_id=TEST_UUID, permissions=[Permission.INSIGHTS])

    service.space_service.get_space.return_value = MagicMock(user_id=uuid4())
    service.user = user
    service.assistant_service.get_assistant.return_value = (
        AsyncMock(space_id=uuid4(), user=service.user),
        MagicMock(),
    )

    from_date = date.today()
    to_date = from_date
    await service.ask_question_on_questions(
        question="Test",
        stream=False,
        assistant_id=uuid4(),
        from_date=from_date,
        to_date=to_date,
    )
