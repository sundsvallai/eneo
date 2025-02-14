<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { invalidate } from "$app/navigation";
  import { getIntric } from "$lib/core/Intric";
  import type { CompletionModel, EmbeddingModel } from "@intric/intric-js";
  import { Input, Tooltip } from "@intric/ui";

  export let model: (CompletionModel | EmbeddingModel) & { is_locked?: boolean | null | undefined };

  const intric = getIntric();

  async function toggleEnabled() {
    const target = "token_limit" in model ? { completionModel: model } : { embeddingModel: model };
    try {
      model = await intric.models.update({
        ...target,
        update: {
          is_org_enabled: !model.is_org_enabled
        }
      });
      invalidate("admin:models:load");
    } catch (e) {
      alert(`Error changing status of ${model.name}`);
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
    <Input.Switch
      sideEffect={toggleEnabled}
      value={model.is_org_enabled}
      disabled={model.is_locked ?? false}
    ></Input.Switch>
  </Tooltip>
</div>
