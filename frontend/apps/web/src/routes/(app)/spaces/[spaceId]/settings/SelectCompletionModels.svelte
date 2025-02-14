<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import type { CompletionModel } from "@intric/intric-js";
  import ModelNameAndVendor from "$lib/features/ai-models/components/ModelNameAndVendor.svelte";
  import { Input } from "@intric/ui";
  import { derived } from "svelte/store";
  import { Settings } from "$lib/components/layout";
  import { sortModels } from "$lib/features/ai-models/sortModels";

  export let selectableModels: CompletionModel[];
  sortModels(selectableModels);

  const {
    state: { currentSpace },
    updateSpace
  } = getSpacesManager();

  const currentlySelectedModels = derived(
    currentSpace,
    ($currentSpace) => $currentSpace.completion_models.map((model) => model.id) ?? []
  );

  let loading = new Set<string>();
  async function toggleModel(model: CompletionModel) {
    loading.add(model.id);
    loading = loading;

    try {
      if ($currentlySelectedModels.includes(model.id)) {
        const newModels = $currentlySelectedModels
          .filter((id) => id !== model.id)
          .map((id) => {
            return { id };
          });
        await updateSpace({ completion_models: newModels });
      } else {
        const newModels = [...$currentlySelectedModels, model.id].map((id) => {
          return { id };
        });
        await updateSpace({ completion_models: newModels });
      }
    } catch (e) {
      alert(e);
    }
    loading.delete(model.id);
    loading = loading;
  }
</script>

<Settings.Row
  title="Completion Models"
  description="Choose which completion models will be available to the applications in this space."
>
  <svelte:fragment slot="description">
    {#if $currentSpace.completion_models.length === 0}
      <p
        class="label-warning mt-2.5 rounded-md border border-label-default bg-label-dimmer px-2 py-1 text-sm text-label-stronger"
      >
        <span class="font-bold">Hint:&nbsp;</span>Enable at least one completion model to be able to
        use assistants.
      </p>
    {/if}
  </svelte:fragment>

  {#each selectableModels as model (model.id)}
    <div class="cursor-pointer border-b border-default py-4 pl-2 pr-4 hover:bg-hover-dimmer">
      <Input.Switch
        value={$currentlySelectedModels.includes(model.id)}
        sideEffect={() => toggleModel(model)}
      >
        <ModelNameAndVendor {model} />
      </Input.Switch>
    </div>
  {/each}
</Settings.Row>
