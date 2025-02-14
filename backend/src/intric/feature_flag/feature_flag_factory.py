from intric.database.tables.feature_flag_table import (
    GlobalFeatureFlag,
    TenantFeatureFlag,
)
from intric.feature_flag.feature_flag import FeatureFlag


class FeatureFlagFactory:
    @classmethod
    def create_domain_feature_flag(
        cls,
        global_feature_flag: GlobalFeatureFlag,
        tenant_feature_flags: list[TenantFeatureFlag],
    ) -> FeatureFlag:
        tenant_ids = set()
        if tenant_feature_flags:
            tenant_ids = {i.tenant_id for i in tenant_feature_flags}

        return FeatureFlag(
            feature_id=global_feature_flag.id,
            name=global_feature_flag.name,
            tenant_ids=tenant_ids,
            is_enabled_globally=global_feature_flag.enabled,
            description=global_feature_flag.description,
        )
