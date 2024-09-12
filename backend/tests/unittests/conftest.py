import uuid

import pytest

from instorage.ai_models.completion_models.completion_model import (
    ModelHostingLocation,
    ModelStability,
)
from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelFamily,
)
from instorage.tenants.tenant import TenantInDB
from instorage.users.user import UserInDB


@pytest.fixture
def embedding_model_small():
    return EmbeddingModel(
        id=uuid.uuid4(),
        name="text-embedding-3-small",
        family=EmbeddingModelFamily.OPEN_AI,
        open_source=False,
        dimensions=512,
        max_input=8191,
        stability=ModelStability.STABLE,
        hosting=ModelHostingLocation.USA,
        is_deprecated=False,
    )


@pytest.fixture
def tenant(embedding_model_small: EmbeddingModel):
    return TenantInDB(
        id=uuid.uuid4(),
        name="test_tenant",
        quota_limit=0,
        quota_used=0,
    )


@pytest.fixture
def user(tenant: TenantInDB):
    return UserInDB(
        id=uuid.uuid4(),
        username="test_user",
        email="test@user.com",
        salt="test_salt",
        password="test_pass",
        used_tokens=0,
        tenant_id=tenant.id,
        quota_used=0,
        tenant=tenant,
    )
