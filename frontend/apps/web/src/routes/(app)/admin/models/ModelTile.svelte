<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import type { CompletionModel, EmbeddingModel } from "@intric/intric-js";
  import ModelEnableSwitch from "./ModelEnableSwitch.svelte";
  import { Label } from "@intric/ui";
  import { getLabels } from "$lib/features/ai-models/components/ModelLabels.svelte";
  import ModelNameAndVendor from "$lib/features/ai-models/components/ModelNameAndVendor.svelte";

  export let model: CompletionModel | EmbeddingModel;
  export let modeltype: "completion" | "embedding";

  let labels = getLabels(model);
</script>

<div
  class="flex w-[24rem] flex-col rounded-xl border border-b-2 border-stone-300 bg-stone-50 shadow"
>
  <div
    class="-m-[1px] flex flex-grow flex-col rounded-lg border border-stone-400/60 bg-white shadow-sm"
  >
    <div class="flex flex-col gap-2 p-4">
      <ModelNameAndVendor {model} size="card"></ModelNameAndVendor>
      <div class="pt-2">
        {model.description}
      </div>
    </div>
    <div class="h-[1px] bg-stone-200"></div>
    <div class="flex flex-col items-start px-4 pb-3 pt-1">
      <Label.List
        content={[
          {
            label: model.name,
            color: "blue",
            tooltip: "Full model name"
          }
        ]}
        capitalize={false}
        monospaced={true}>Full name</Label.List
      >
      <Label.List content={labels}>Details</Label.List>
    </div>
  </div>
  <div>
    <div class="flex h-full items-center justify-between px-5 py-4">
      <p>Enabled</p>
      <ModelEnableSwitch {model} {modeltype} />
    </div>
  </div>
</div>
