<!-- MIT License -->

<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import type { EmbeddingModel } from "@intric/intric-js";
  import ModelNameAndVendor from "$lib/features/ai-models/components/ModelNameAndVendor.svelte";
  import { Input } from "@intric/ui";
  import { derived } from "svelte/store";

  export let selectableModels: EmbeddingModel[];
  selectableModels.sort(sortModel);

  function sortModel(a: EmbeddingModel, b: EmbeddingModel) {
    if (a.org === b.org) {
      return (a.name ?? "a") > (b.name ?? "b") ? 1 : -1;
    }
    return (a.org ?? "a") > (b.org ?? "b") ? 1 : -1;
  }

  const {
    state: { currentSpace },
    updateSpace
  } = getSpacesManager();

  const currentlySelectedModels = derived(
    currentSpace,
    ($currentSpace) => $currentSpace.embedding_models.map((model) => model.id) ?? []
  );

  let loading = new Set<string>();
  async function toggleModel(model: EmbeddingModel) {
    loading.add(model.id);
    loading = loading;

    try {
      if ($currentlySelectedModels.includes(model.id)) {
        const newModels = $currentlySelectedModels
          .filter((id) => id !== model.id)
          .map((id) => {
            return { id };
          });
        await updateSpace({ embedding_models: newModels });
      } else {
        const newModels = [...$currentlySelectedModels, model.id].map((id) => {
          return { id };
        });
        await updateSpace({ embedding_models: newModels });
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
    <h3 class="pb-1 text-lg font-medium">Embedding Models</h3>
    <p class="text-stone-500">
      Choose which embedding models will be available to embed data in this space.
    </p>
    {#if $currentSpace.embedding_models.length === 0}
      <p
        class="mt-2.5 rounded-md border border-amber-500 bg-amber-50 px-2 py-1 text-sm text-amber-800"
      >
        <span class="font-bold">Hint:&nbsp;</span>Enable an emedding model to be able to use
        knowledge from collections and websites.
      </p>
    {:else if $currentSpace.embedding_models.length > 1}
      <p
        class="mt-2.5 rounded-md border border-amber-500 bg-amber-50 px-2 py-1 text-sm text-amber-800"
      >
        <span class="font-bold">Hint:&nbsp;</span>We strongly recommend to only activate one
        embedding model per space. Data embedded with different models is not compatible with each
        other.
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
