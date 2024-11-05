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

  export let selectableModels: CompletionModel[];
  selectableModels.sort(sortModel);

  function sortModel(a: CompletionModel, b: CompletionModel) {
    if (a.org === b.org) {
      return (a.nickname ?? "a") > (b.nickname ?? "b") ? 1 : -1;
    }
    return (a.org ?? "a") > (b.org ?? "b") ? 1 : -1;
  }

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

<div class="flex flex-col gap-4 pb-2 lg:flex-row lg:gap-12">
  <div class="pl-2 pr-12 lg:w-2/5">
    <h3 class="pb-1 text-lg font-medium">Completion Models</h3>
    <p class="text-stone-500">
      Choose which completion models will be available to the applications in this space.
    </p>
    {#if $currentSpace.completion_models.length === 0}
      <p
        class="mt-2.5 rounded-md border border-amber-500 bg-amber-50 px-2 py-1 text-sm text-amber-800"
      >
        <span class="font-bold">Hint:&nbsp;</span>Enable at least one completion model to be able to
        use assistants.
      </p>
    {/if}
  </div>

  <div class="flex flex-grow flex-col">
    {#each selectableModels as model (model.id)}
      <div class=" cursor-pointer border-b border-black/10 py-4 pl-2 pr-4 hover:bg-stone-50">
        <Input.Switch
          value={$currentlySelectedModels.includes(model.id)}
          sideEffect={() => toggleModel(model)}
        >
          <ModelNameAndVendor {model} />
        </Input.Switch>
      </div>
    {/each}
  </div>
</div>
