from unittest.mock import AsyncMock, MagicMock

from intric.ai_models.completion_models.context_builder import count_tokens
from intric.apps.app_runs.app_run_service import AppRunService


async def test_update_tokens_in_run():
    # Setup
    app_run_service = AppRunService(
        MagicMock(id=1), AsyncMock(), MagicMock(), AsyncMock(), AsyncMock(), AsyncMock()
    )

    app_run = MagicMock(user_id=1)
    app_run_service.repo.get.return_value = app_run

    completion = "This is the output!"
    app_run_service.app_service.run_app.return_value = MagicMock(
        completion=completion, total_token_count=10
    )

    # Execute
    await app_run_service.run_app(MagicMock(), MagicMock(), MagicMock(), MagicMock())

    # Assert
    num_tokens_output = count_tokens(completion)
    app_run.update.assert_called_once_with(
        output=completion,
        num_tokens_input=10,
        num_tokens_output=num_tokens_output,
    )
