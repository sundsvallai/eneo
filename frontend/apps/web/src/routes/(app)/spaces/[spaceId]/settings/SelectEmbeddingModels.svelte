<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import type { EmbeddingModel } from "@intric/intric-js";
  import ModelNameAndVendor from "$lib/features/ai-models/components/ModelNameAndVendor.svelte";
  import { Input } from "@intric/ui";
  import { derived } from "svelte/store";
  import { Settings } from "$lib/components/layout";
  import { sortModels } from "$lib/features/ai-models/sortModels";

  export let selectableModels: EmbeddingModel[];
  sortModels(selectableModels);

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

<Settings.Row
  title="Embedding Models"
  description="Choose which embedding models will be available to embed data in this space."
>
  <svelte:fragment slot="description">
    {#if $currentSpace.embedding_models.length === 0}
      <p
        class="label-warning mt-2.5 rounded-md border border-label-default bg-label-dimmer px-2 py-1 text-sm text-label-stronger"
      >
        <span class="font-bold">Hint:&nbsp;</span>Enable an emedding model to be able to use
        knowledge from collections and websites.
      </p>
    {:else if $currentSpace.embedding_models.length > 1}
      <p
        class="label-warning mt-2.5 rounded-md border border-label-default bg-label-dimmer px-2 py-1 text-sm text-label-stronger"
      >
        <span class="font-bold">Hint:&nbsp;</span>We strongly recommend to only activate one
        embedding model per space. Data embedded with different models is not compatible with each
        other.
      </p>
    {/if}
  </svelte:fragment>

  {#each selectableModels as model (model.id)}
    <div class=" cursor-pointer border-b border-default py-4 pl-2 pr-4 hover:bg-hover-dimmer">
      <Input.Switch
        value={$currentlySelectedModels.includes(model.id)}
        sideEffect={() => toggleModel(model)}
      >
        <ModelNameAndVendor {model} />
      </Input.Switch>
    </div>
  {/each}
</Settings.Row>
