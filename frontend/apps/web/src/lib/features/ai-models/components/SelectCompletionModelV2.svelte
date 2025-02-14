<script lang="ts">
  import type { CompletionModel } from "@intric/intric-js";
  import ModelNameAndVendor from "./ModelNameAndVendor.svelte";
  import { sortModels } from "../sortModels";
  import { createSelect } from "@melt-ui/svelte";
  import { IconCheck } from "@intric/icons/check";
  import { IconCancel } from "@intric/icons/cancel";
  import { IconChevronDown } from "@intric/icons/chevron-down";

  /** An array of models the user can choose from, this component will sort in-place the models by vendor */
  export let availableModels: CompletionModel[];
  sortModels(availableModels);
  /** Bindable id of the selected model*/
  export let selectedModel: CompletionModel | undefined | null;

  export let aria: AriaProps = { "aria-label": "Select completion model" };

  const {
    elements: { trigger, menu, option },
    states: { selected },
    helpers: { isSelected }
  } = createSelect<CompletionModel>({
    positioning: {
      placement: "bottom",
      fitViewport: true,
      sameWidth: true
    },
    defaultSelected: selectedModel ? { value: selectedModel } : undefined,
    portal: null,
    onSelectedChange: ({ next }) => {
      selectedModel = next?.value ?? availableModels[0];
      return next;
    }
  });

  $: unsupportedModelSelected = !availableModels.some((model) => model.id === selectedModel?.id);

  function watchChanges(incomingModel: CompletionModel | null | undefined) {
    if ($selected?.value !== incomingModel) {
      $selected = incomingModel ? { value: incomingModel } : undefined;
    }
  }
  // Watch outside changes
  $: watchChanges(selectedModel);
</script>

<button
  {...$trigger}
  {...aria}
  use:trigger
  class="flex h-16 items-center justify-between border-b border-default px-4 hover:bg-hover-default"
>
  {#if unsupportedModelSelected}
    <div class="flex gap-3 truncate pl-1 text-negative-default">
      <IconCancel />Unsupported model selected ({selectedModel?.name ?? "No model found"})
    </div>
  {:else if $selected}
    <ModelNameAndVendor model={$selected.value}></ModelNameAndVendor>
  {:else}
    <div class="flex gap-3 truncate pl-1 text-negative-default">
      <IconCancel />No model selected
    </div>
  {/if}
  <IconChevronDown />
</button>

<div
  class="z-20 flex flex-col overflow-y-auto rounded-lg border border-default bg-primary shadow-xl"
  {...$menu}
  use:menu
>
  <div
    class="bg-frosted-glass-secondary sticky top-0 border-b border-default px-4 py-2 font-mono text-sm"
  >
    Select a completion model
  </div>
  {#each availableModels as model}
    <div
      class="flex min-h-16 items-center justify-between border-b border-default px-4 hover:cursor-pointer hover:bg-hover-default"
      {...$option({ value: model, label: model.nickname })}
      use:option
    >
      <ModelNameAndVendor {model}></ModelNameAndVendor>
      <div class="check {$isSelected(model) ? 'block' : 'hidden'}">
        <IconCheck class="text-positive-default" />
      </div>
    </div>
  {/each}
</div>

<style lang="postcss">
  div[data-highlighted] {
    @apply bg-hover-default;
  }

  /* div[data-selected] { } */

  div[data-disabled] {
    @apply opacity-30 hover:bg-transparent;
  }
</style>
