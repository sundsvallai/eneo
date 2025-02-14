<script lang="ts">
  import { IconCheck } from "@intric/icons/check";
  import { IconChevronUpDown } from "@intric/icons/chevron-up-down";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { createSelect } from "@melt-ui/svelte";
  import { fly } from "svelte/transition";
  import { quadInOut } from "svelte/easing";
  import ModelNameAndVendor from "$lib/features/ai-models/components/ModelNameAndVendor.svelte";
  import { sortModels } from "$lib/features/ai-models/sortModels";
  const {
    state: { currentSpace },
    updateDefaultAssistant
  } = getSpacesManager();

  const {
    elements: { trigger, menu, option },
    helpers: { isSelected }
  } = createSelect<{ id: string }>({
    positioning: {
      placement: "bottom-start",
      fitViewport: true
    },
    defaultSelected: $currentSpace.default_assistant.completion_model
      ? { value: { id: $currentSpace.default_assistant.completion_model.id } }
      : undefined,
    onSelectedChange: ({ next }) => {
      if (next) {
        updateDefaultAssistant({ completionModel: next.value });
      }
      return next;
    }
  });
</script>

<button
  {...$trigger}
  use:trigger
  in:fly|global={{ x: -5, duration: parent ? 300 : 0, easing: quadInOut, opacity: 0.3 }}
  class=" group flex max-w-[calc(100%_-_4rem)] items-center justify-between gap-2 overflow-hidden rounded-lg border border-default py-1 pl-2 pr-1 text-[1.4rem] font-extrabold leading-normal text-primary hover:border-dimmer hover:bg-hover-default"
>
  <span class="truncate text-base font-medium">
    {#if $currentSpace.default_assistant.completion_model}
      {$currentSpace.default_assistant.completion_model.nickname}
    {:else}
      Select a model...
    {/if}
  </span>
  <IconChevronUpDown class="min-w-6 text-secondary group-hover:text-primary" />
</button>

<div
  class="z-10 flex min-w-[24vw] flex-col overflow-y-auto rounded-lg border border-default bg-primary shadow-xl"
  {...$menu}
  use:menu
>
  <div
    class="bg-frosted-glass-secondary sticky top-0 border-b border-default px-4 py-2 pr-12 font-mono text-sm"
  >
    Choose a completion model
  </div>
  {#each sortModels($currentSpace.completion_models) as model}
    <div
      class="flex min-h-16 items-center gap-4 border-b border-default px-4 hover:cursor-pointer hover:bg-hover-default"
      {...$option({ value: { id: model.id } })}
      use:option
    >
      <ModelNameAndVendor {model}></ModelNameAndVendor>
      <div class="flex-grow"></div>
      <div class="check {$isSelected({ id: model.id }) ? 'block' : 'hidden'}">
        <IconCheck class="!size-8 text-positive-stronger"></IconCheck>
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
