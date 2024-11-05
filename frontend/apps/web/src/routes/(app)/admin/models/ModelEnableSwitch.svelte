<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { invalidate } from "$app/navigation";
  import { getIntric } from "$lib/core/Intric";
  import { Input, Tooltip } from "@intric/ui";

  export let model: { id: string; is_org_enabled?: boolean; is_locked?: boolean };
  export let modeltype: "completion" | "embedding";

  const intric = getIntric();

  async function updateCompletionModel(
    completionModel: { id: string },
    update: { is_org_enabled: boolean }
  ) {
    try {
      await intric.models.update({ completionModel, update });
      invalidate("admin:models:load");
    } catch (e) {
      alert(e);
      console.error(e);
    }
  }

  async function updateEmbeddingModel(
    embeddingModel: { id: string },
    update: { is_org_enabled: boolean }
  ) {
    try {
      await intric.models.update({ embeddingModel, update });
      invalidate("admin:models:load");
    } catch (e) {
      alert(e);
      console.error(e);
    }
  }

  async function updateModel({ next }: { next: boolean }) {
    if (modeltype == "completion") {
      await updateCompletionModel({ id: model.id }, { is_org_enabled: next });
    } else {
      await updateEmbeddingModel({ id: model.id }, { is_org_enabled: next });
    }
  }

  $: tooltip = model.is_locked
    ? "EU-hosted models are available on request"
    : model.is_org_enabled
      ? "Toggle to disable model"
      : "Toggle to enable model";
</script>

<div class="-ml-3 flex items-center gap-4">
  <Tooltip text={tooltip}>
    <Input.Switch sideEffect={updateModel} value={model.is_org_enabled} disabled={model.is_locked}
    ></Input.Switch>
  </Tooltip>
</div>
