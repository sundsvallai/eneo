<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconChevronUpDown } from "@intric/icons/chevron-up-down";
  import { IconSelectedItem } from "@intric/icons/selected-item";
  import { IconSquare } from "@intric/icons/square";
  import { Button, Dialog } from "@intric/ui";
  import { createDropdownMenu } from "@melt-ui/svelte";
  import { getSpacesManager } from "../SpacesManager";
  import { fade, fly } from "svelte/transition";
  import SpaceChip from "./SpaceChip.svelte";
  import CreateSpaceDialog from "./CreateSpaceDialog.svelte";

  export let showSelectPrompt = false;

  const spaces = getSpacesManager();
  const {
    state: { currentSpace, accessibleSpaces }
  } = spaces;

  const {
    elements: { trigger, menu, item, overlay, arrow },
    states: { open }
  } = createDropdownMenu({
    forceVisible: true,
    portal: null,
    loop: true,
    positioning: {
      placement: "bottom-start",
      overlap: true,
      overflowPadding: 0
    },
    arrowSize: 12
  });

  let showCreateDialog: Dialog.OpenState;
</script>

{#if $currentSpace.personal && !showSelectPrompt}
  <div
    class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b-[0.5px] border-default pl-[1.4rem] pr-5 pt-0.5 font-medium"
  >
    <SpaceChip space={$currentSpace}></SpaceChip>
    <span class="flex-grow truncate pl-0.5 text-left text-primary"> Personal space </span>
  </div>
{:else}
  <Button
    is={[$trigger]}
    unstyled
    label="Change space or create a new one"
    class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b-[0.5px] border-default pl-[1.4rem] pr-5 pt-0.5 font-medium hover:bg-accent-dimmer hover:text-accent-stronger"
  >
    {#if showSelectPrompt}
      <div
        class="flex min-h-[1.6rem] min-w-[1.6rem] items-center justify-center rounded-md bg-dynamic-dimmer text-dynamic-stronger"
      >
        <IconSquare />
      </div>
      <span class="flex-grow truncate pl-0.5 text-left text-primary"> Select a space </span>
    {:else}
      <SpaceChip space={$currentSpace}></SpaceChip>
      <span class="flex-grow truncate pl-0.5 text-left text-primary">
        {$currentSpace.name}
      </span>
    {/if}
    <IconChevronUpDown class="min-w-6 text-muted group-hover:text-accent-stronger" />
  </Button>
{/if}

<!-- Selector drop down -->
{#if $open}
  <div
    {...$overlay}
    use:overlay
    class="fixed inset-0 z-[70] bg-overlay-dimmer"
    transition:fade={{ duration: 200 }}
  />
  <div
    {...$menu}
    use:menu
    in:fly={{ y: -15, duration: 100 }}
    out:fly={{ y: -5, duration: 200 }}
    class="items absolute z-[80] flex min-w-[17rem] -translate-x-0.5 -translate-y-[0.78rem] flex-col rounded-sm bg-primary p-3 shadow-md"
  >
    <div
      class="flex items-baseline justify-between gap-4 border-b border-default pb-2.5 pl-6 pr-3 pt-1 font-mono text-[0.85rem] font-medium tracking-[0.015rem] text-secondary"
    >
      <a href="/spaces/list" class="hover:underline"> Your spaces </a>
    </div>

    <div class="relative max-h-[50vh] overflow-y-auto">
      {#each $accessibleSpaces as space}
        {#if !space.personal}
          <Button
            unstyled
            is={[$item]}
            href="/spaces/{space.id}/overview"
            class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b border-default pl-5 pr-4 last-of-type:border-b-0 hover:bg-accent-dimmer hover:text-accent-stronger"
          >
            <SpaceChip {space}></SpaceChip>

            <span class="flex-grow truncate text-left">
              {space.name}
            </span>
            <div class="ml-2 min-w-5 text-accent-stronger">
              {#if space.id === $currentSpace.id && !showSelectPrompt}
                <IconSelectedItem />
              {/if}
            </div>
          </Button>
        {/if}
      {/each}
    </div>
    <Button
      unstyled
      on:click={() => {
        $showCreateDialog = true;
      }}
      is={[$item]}
      class="mt-1 !justify-center rounded-lg border border-default bg-accent-default !py-2 text-on-fill shadow-md hover:bg-accent-stronger focus:outline-offset-4 focus:ring-offset-4"
      >Create a new space</Button
    >
    <div {...$arrow} use:arrow class="!z-10 border-stronger" />
  </div>
{/if}

<CreateSpaceDialog includeTrigger={false} forwardToNewSpace={true} bind:isOpen={showCreateDialog}
></CreateSpaceDialog>

<style>
  .items {
    box-shadow:
      0px 10px 20px -10px rgba(0, 0, 0, 0.5),
      0px 30px 50px 0px rgba(0, 0, 0, 0.2);
  }
</style>
