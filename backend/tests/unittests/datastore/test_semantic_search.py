from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from intric.ai_models.embedding_models.datastore.datastore import Datastore
from tests.fixtures import TEST_GROUP


@pytest.fixture(name="datastore")
def datastore_with_mocks():
    return Datastore(
        user=MagicMock(),
        info_blob_chunk_repo=AsyncMock(),
        embedding_model_adapter=AsyncMock(),
    )


async def test_semantic_search(datastore: Datastore):
    with patch(
        "intric.ai_models.embedding_models.datastore.datastore.autocut",
    ) as autocut_mock:

        await datastore.semantic_search(search_string="giraffe", groups=[TEST_GROUP])
        autocut_mock.assert_not_called()

        await datastore.semantic_search(
            search_string="giraffe", groups=[TEST_GROUP], autocut_cutoff=1
        )
        autocut_mock.assert_called_once()
