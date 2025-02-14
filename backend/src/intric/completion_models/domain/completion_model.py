from enum import Enum
from typing import TYPE_CHECKING, Optional

from intric.main.config import SETTINGS
from intric.modules.module import Modules

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID

    from intric.users.user import UserInDB


class ModelFamily(str, Enum):
    OPEN_AI = "openai"
    MISTRAL = "mistral"
    VLLM = "vllm"
    CLAUDE = "claude"
    AZURE = "azure"


class ModelStability(str, Enum):
    STABLE = "stable"
    EXPERIMENTAL = "experimental"


class ModelHostingLocation(str, Enum):
    USA = "usa"
    EU = "eu"
    SWE = "swe"


class ModelOrg(str, Enum):
    OPENAI = "OpenAI"
    META = "Meta"
    MICROSOFT = "Microsoft"
    ANTHROPIC = "Anthropic"


class CompletionModel:
    def __init__(
        self,
        user: "UserInDB",
        id: "UUID",
        created_at: "datetime",
        updated_at: "datetime",
        name: str,
        model_name: str,
        token_limit: int,
        vision: bool,
        family: ModelFamily,
        hosting: ModelHostingLocation,
        org: Optional[ModelOrg],
        stability: ModelStability,
        open_source: bool,
        description: Optional[str],
        nr_billion_parameters: Optional[int],
        hf_link: Optional[str],
        is_deprecated: bool,
        deployment_name: Optional[str],
        is_org_enabled: bool,
        is_org_default: bool,
    ):
        self.user = user
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name
        self.model_name = model_name
        self.token_limit = token_limit
        self.vision = vision
        self.family = family
        self.hosting = hosting
        self.org = org
        self.stability = stability
        self.open_source = open_source
        self.description = description
        self.nr_billion_parameters = nr_billion_parameters
        self.hf_link = hf_link
        self.is_deprecated = is_deprecated
        self.deployment_name = deployment_name
        self.is_org_enabled = is_org_enabled
        self.is_org_default = is_org_default

    @property
    def is_locked(self):
        if self.hosting == ModelHostingLocation.EU:
            if Modules.EU_HOSTING not in self.user.modules:
                return True

        if self.family == ModelFamily.AZURE:
            if not SETTINGS.using_azure_models:
                return True

        return False

    @property
    def can_access(self):
        return not self.is_locked and not self.is_deprecated and self.is_org_enabled
