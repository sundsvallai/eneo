from typing import TYPE_CHECKING

from intric.integration.presentation.models import (
    IntegrationPreviewData,
    IntegrationPreviewDataList,
)

if TYPE_CHECKING:
    from intric.integration.domain.entities.integration_preview import (
        IntegrationPreview,
    )


class ConfluenceContentAssembler:
    @classmethod
    def to_model(self, item: "IntegrationPreview") -> "IntegrationPreviewData":
        return IntegrationPreviewData(
            key=item.key,
            type=item.type,
            name=item.name,
            url=item.url,
        )

    @classmethod
    def to_paginated_response(
        self,
        items: list["IntegrationPreview"],
    ) -> IntegrationPreviewDataList:
        items = [self.to_model(i) for i in items]
        return IntegrationPreviewDataList(items=items)
