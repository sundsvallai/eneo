from uuid import uuid4

from intric.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelFamily,
    ModelHostingLocation,
    ModelStability,
)
from intric.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelFamily,
)
from intric.assistants.assistant import Assistant
from intric.authentication.auth_models import ApiKey
from intric.groups.api.group_models import Group
from intric.roles.permissions import Permission
from intric.roles.role import RoleInDB
from intric.tenants.tenant import TenantInDB
from intric.users.user import UserInDB

TEST_UUID = uuid4()

TEST_EMBEDDING_MODEL = EmbeddingModel(
    id=uuid4(),
    name="text-embedding-3-small-test",
    family=EmbeddingModelFamily.OPEN_AI,
    open_source=False,
    dimensions=512,
    max_input=8191,
    stability=ModelStability.STABLE,
    hosting=ModelHostingLocation.USA,
    is_deprecated=False,
)

TEST_EMBEDDING_MODEL_ADA = EmbeddingModel(
    id=uuid4(),
    name="text-embedding-ada-002-test",
    family=EmbeddingModelFamily.OPEN_AI,
    open_source=False,
    max_input=8191,
    stability=ModelStability.STABLE,
    hosting=ModelHostingLocation.USA,
    is_deprecated=False,
)

TEST_TENANT = TenantInDB(
    id=uuid4(),
    name="test_tenant",
    quota_limit=1024**3,
)
TEST_TENANT_2 = TenantInDB(
    id=uuid4(),
    name="test_tenant_2",
    quota_limit=1024**3,
)
TEST_API_KEY = ApiKey(key="supersecret", truncated_key="cret")
TEST_ROLE = RoleInDB(
    id=uuid4(),
    name="God",
    permissions=[permission for permission in Permission],
    tenant_id=TEST_TENANT.id,
)
TEST_USER = UserInDB(
    id=uuid4(),
    username="test_user",
    email="test@user.com",
    salt="test_salt",
    password="test_pass",
    used_tokens=0,
    tenant_id=TEST_TENANT.id,
    quota_limit=20000,
    tenant=TEST_TENANT,
    user_groups=[],
    roles=[TEST_ROLE],
    state="active",
)


TEST_USER_2 = UserInDB(
    id=uuid4(),
    username="test_user_3",
    email="test3@user.com",
    salt="test_salt",
    password="test_pass",
    used_tokens=0,
    tenant_id=TEST_TENANT_2.id,
    tenant=TEST_TENANT_2,
    roles=[TEST_ROLE],
    state="active",
)
TEST_MODEL_GPT4 = CompletionModel(
    id=uuid4(),
    name="gpt-4-turbo",
    nickname="GPT-4",
    family=CompletionModelFamily.OPEN_AI,
    token_limit=4000,
    is_deprecated=False,
    stability=ModelStability.STABLE,
    hosting=ModelHostingLocation.USA,
    vision=True,
)

TEST_MODEL_CHATGPT = CompletionModel(
    id=uuid4(),
    name="gpt-3.5-turbo",
    nickname="ChatGPT",
    family=CompletionModelFamily.OPEN_AI,
    token_limit=16385,
    is_deprecated=False,
    stability=ModelStability.STABLE,
    hosting=ModelHostingLocation.USA,
    vision=False,
)


TEST_MODEL_MIXTRAL = CompletionModel(
    id=uuid4(),
    name="Mixtral",
    nickname="Mixtral",
    family=CompletionModelFamily.MISTRAL,
    token_limit=16384,
    is_deprecated=True,
    stability=ModelStability.EXPERIMENTAL,
    hosting=ModelHostingLocation.EU,
    vision=False,
)

TEST_MODEL_EU = CompletionModel(
    id=uuid4(),
    name="Mixtral",
    nickname="Mixtral",
    family=CompletionModelFamily.MISTRAL,
    token_limit=16384,
    is_deprecated=False,
    stability=ModelStability.EXPERIMENTAL,
    hosting=ModelHostingLocation.EU,
    vision=False,
)

TEST_MODEL_AZURE = CompletionModel(
    id=uuid4(),
    name="azure model",
    nickname="azure model",
    family=CompletionModelFamily.AZURE,
    token_limit=128000,
    is_deprecated=False,
    stability=ModelStability.STABLE,
    hosting=ModelHostingLocation.USA,
    vision=True,
)


TEST_GROUP = Group(
    id=uuid4(),
    space_id=TEST_UUID,
    name="test_group",
    size=0,
    published=False,
    user_id=TEST_USER.id,
    user=TEST_USER,
    tenant_id=TEST_TENANT.id,
    is_public=False,
    embedding_model_id=TEST_EMBEDDING_MODEL.id,
    embedding_model=TEST_EMBEDDING_MODEL,
)


TEST_ASSISTANT = Assistant(
    id=uuid4(),
    space_id=TEST_UUID,
    name="test_assistant",
    prompt="test_prompt",
    completion_model=TEST_MODEL_CHATGPT,
    completion_model_kwargs={},
    user=TEST_USER,
    logging_enabled=False,
    websites=[],
    groups=[TEST_GROUP],
    attachments=[],
    published=False,
)
