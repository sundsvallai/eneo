<script lang="ts">
  import { IconCheck } from "@intric/icons/check";
  import { IconChevronUpDown } from "@intric/icons/chevron-up-down";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { createSelect } from "@melt-ui/svelte";
  import { getChatManager } from "../../ChatManager";
  import SpaceChip from "$lib/features/spaces/components/SpaceChip.svelte";
  import { goto } from "$app/navigation";
  import { fly } from "svelte/transition";
  import { quadInOut } from "svelte/easing";
  import { formatEmojiTitle } from "$lib/core/formatting/formatEmojiTitle";

  const {
    state: { currentSpace }
  } = getSpacesManager();
  const {
    state: { assistant }
  } = getChatManager();

  const {
    elements: { trigger, menu, option },
    helpers: { isSelected }
  } = createSelect<{ id: string }>({
    positioning: {
      placement: "bottom-start",
      fitViewport: true
    },
    defaultSelected: { value: { id: $assistant.id } },
    onSelectedChange: ({ next }) => {
      if (next) {
        goto(`/spaces/${$currentSpace.routeId}/assistants/${next.value.id}`);
      }
      return next;
    }
  });
</script>

<button
  {...$trigger}
  use:trigger
  in:fly|global={{ x: -5, duration: parent ? 300 : 0, easing: quadInOut, opacity: 0.3 }}
  class="group flex max-w-[calc(100%_-_1rem)] items-center justify-between gap-2 overflow-hidden rounded-lg border border-transparent py-0.5 pl-2 pr-1 text-[1.4rem] font-extrabold leading-normal text-primary hover:border-dimmer hover:bg-hover-default"
>
  <span class="truncate">{$assistant.name}</span>
  <!-- translate-y to make it look on the same line as the chevron in the space selector -->
  <IconChevronUpDown
    class="min-w-6 translate-y-[0.05rem] text-secondary group-hover:text-primary"
  />
</button>

<div
  class="z-10 flex min-w-[24vw] flex-col overflow-y-auto rounded-lg border border-default bg-primary shadow-xl"
  {...$menu}
  use:menu
>
  <div
    class="bg-frosted-glass-secondary sticky top-0 border-b border-default px-4 py-2 pr-12 font-mono text-sm"
  >
    Select an assistant
  </div>
  {#each $currentSpace.applications.assistants as assistant}
    <div
      class="flex min-h-16 items-center gap-4 border-b border-default px-4 hover:cursor-pointer hover:bg-hover-default"
      {...$option({ value: { id: assistant.id } })}
      use:option
    >
      <SpaceChip space={{ ...assistant, personal: false }}></SpaceChip>
      {formatEmojiTitle(assistant.name)}
      <div class="flex-grow"></div>
      <div class="check {$isSelected({ id: assistant.id }) ? 'block' : 'hidden'}">
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
