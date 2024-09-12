from unittest.mock import AsyncMock

from instorage.services.service import DatastoreResult, RunnerResult
from instorage.workflows.assistant_guard_runner import AssistantGuardRunner
from instorage.workflows.filters import ContinuationFilter
from instorage.workflows.steps import Step


async def test_run_guard_workflow():
    service_runner = AsyncMock()
    service_runner.run.return_value = RunnerResult(
        result=True,
        datastore_result=DatastoreResult(
            chunks=[], no_duplicate_chunks=[], info_blobs=[]
        ),
    )
    assistant_runner = AsyncMock()
    session_service = AsyncMock()

    async def it():
        for i in range(10):
            yield i

    assistant_runner.run.return_value = it()
    cont_filter = ContinuationFilter(
        chain_breaker_message="Sorry I can only answer questions about cheese"
    )
    step = Step(runner=service_runner, filter=cont_filter)

    workflow = AssistantGuardRunner(
        assistant_runner=assistant_runner,
        guard_step=step,
        session_service=session_service,
    )

    output = await workflow.run("This is normal user input", stream=True)

    async for i in output:
        assert isinstance(i, int)
