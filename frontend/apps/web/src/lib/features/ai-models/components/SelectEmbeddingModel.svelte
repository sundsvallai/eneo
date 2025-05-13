<script lang="ts">
  import type { EmbeddingModel } from "@intric/intric-js";
  import { Select } from "@intric/ui";
  import { writable, type Writable } from "svelte/store";

  // Id of currently selected Embedding Model
  export let value: { id: string } | null | undefined;
  export let selectableModels: EmbeddingModel[];
  export let disabled: boolean = false;
  export let hideWhenNoOptions: boolean = false;

  const stableModels = selectableModels.filter((model) => model.stability === "stable");

  const experimentalModels = selectableModels.filter((model) => model.stability === "experimental");

  let modelSelectStore: Writable<{ value: EmbeddingModel; label: string }>;

  function getModelDisplayName(model: EmbeddingModel) {
    if (model.open_source) {
      return `${model.name} (Open Source)`;
    }
    return model.name;
  }

  let unsupportedModelSelected = false;

  if (value) {
    const selectedModel = selectableModels.find((model) => model.id === value!.id);
    if (!selectedModel) {
      unsupportedModelSelected = true;
      setTimeout(() => {
        alert(
          "This collection's embedding model is no longer supported. Please change it in the assistants settings."
        );
      }, 400);
    }
    modelSelectStore = writable({
      value: selectedModel!,
      label: getModelDisplayName(selectedModel!)
    });
  } else {
    // We assume stable models will always be there, this could be set to some default?
    modelSelectStore = writable({
      value: selectableModels[0],
      label: selectableModels[0] ? getModelDisplayName(selectableModels[0]) : "No model selected"
    });
  }

  function setValue(currentlySelected: { value: EmbeddingModel; label: string } | undefined) {
    if (currentlySelected && currentlySelected.value) {
      value = { id: currentlySelected.value.id };
    }
  }

  $: setValue($modelSelectStore);
</script>

{#if !(hideWhenNoOptions && selectableModels.length < 2)}
  <Select.Root
    {disabled}
    customStore={modelSelectStore}
    class="border-dimmer hover:bg-hover-dimmer border-b px-4 py-4"
  >
    <Select.Label>Embedding model</Select.Label>
    <Select.Trigger placeholder="Select..." error={unsupportedModelSelected}></Select.Trigger>
    <Select.Options>
      <Select.OptionGroup label="Stable Embedding models">
        {#each stableModels as model (model.id)}
          {@const modelName = getModelDisplayName(model)}
          <Select.Item value={model} label={modelName}>
            <div class="flex w-full items-center justify-between py-1">
              <span>
                {modelName}
              </span>
            </div>
          </Select.Item>
        {/each}
        {#if !stableModels.length}
          <Select.Item disabled label="No enabled embedding models for this space" value={null}
          ></Select.Item>
        {/if}
      </Select.OptionGroup>
      {#if experimentalModels.length > 0}
        <Select.OptionGroup label="Experimental Embedding models">
          {#each experimentalModels as model (model.id)}
            {@const modelName = getModelDisplayName(model)}
            <Select.Item value={model} label={modelName}>
              <div class="flex w-full items-center justify-between py-1">
                <span>
                  {modelName}
                </span>
              </div>
            </Select.Item>
          {/each}
        </Select.OptionGroup>
      {/if}
    </Select.Options>
  </Select.Root>
{/if}
