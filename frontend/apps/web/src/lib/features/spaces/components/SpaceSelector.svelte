<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->
<script lang="ts">
  import { createDropdownMenu } from "@melt-ui/svelte";
  import { getSpacesManager } from "../SpacesManager";
  import { fade, fly } from "svelte/transition";
  import { Button, Dialog } from "@intric/ui";
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
    class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b-[0.5px] border-black/15 pl-[1.4rem] pr-5 pt-0.5 font-medium"
  >
    <SpaceChip space={$currentSpace}></SpaceChip>
    <span class="flex-grow truncate pl-0.5 text-left"> Personal space </span>
  </div>
{:else}
  <Button
    is={[$trigger]}
    unstyled
    label="Change space or create a new one"
    class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b-[0.5px] border-black/15  pl-[1.4rem] pr-5 pt-0.5 font-medium hover:bg-blue-100 hover:text-blue-800"
  >
    {#if showSelectPrompt}
      <div
        class="flex min-h-[1.6rem] min-w-[1.6rem] items-center justify-center rounded-md bg-[var(--space-color-light)] text-[var(--space-color)]"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.3"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-[1.12rem] w-[1.12rem]"
          ><path d="M3 7V5a2 2 0 0 1 2-2h2" /><path d="M17 3h2a2 2 0 0 1 2 2v2" /><path
            d="M21 17v2a2 2 0 0 1-2 2h-2"
          /><path d="M7 21H5a2 2 0 0 1-2-2v-2" /></svg
        >
      </div>

      <span class="flex-grow truncate pl-0.5 text-left"> Select a space </span>
    {:else}
      <SpaceChip space={$currentSpace}></SpaceChip>
      <span class="flex-grow truncate pl-0.5 text-left">
        {$currentSpace.name}
      </span>
    {/if}
    <div class="min-w-5">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class=" h-5 w-5 text-black/20 group-hover:text-blue-800/50"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"
        />
      </svg>
    </div>
  </Button>
{/if}

<!-- Selector drop down -->
{#if $open}
  <div
    {...$overlay}
    use:overlay
    class="fixed inset-0 z-[70] bg-black/15"
    transition:fade={{ duration: 200 }}
  />
  <div
    {...$menu}
    use:menu
    in:fly={{ y: -15, duration: 100 }}
    out:fly={{ y: -5, duration: 200 }}
    class="items absolute z-[80] flex min-w-[17rem] -translate-x-0.5 -translate-y-[0.78rem] flex-col rounded-sm border-b border-black/40 bg-white p-3 shadow-md"
  >
    <div
      class="flex items-baseline justify-between gap-4 border-b border-black/10 pb-2.5 pl-6 pr-3 pt-1 font-mono text-[0.85rem] font-medium tracking-[0.015rem] text-black/75"
    >
      <a href="/spaces/list" class="hover:underline"> Your spaces </a>
    </div>

    {#each $accessibleSpaces as space}
      {#if !space.personal}
        <Button
          unstyled
          is={[$item]}
          href="/spaces/{space.id}"
          class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b border-black/10 pl-5 pr-4 last-of-type:border-b-0 hover:bg-blue-100 hover:text-blue-800"
        >
          <SpaceChip {space}></SpaceChip>

          <span class="flex-grow truncate text-left">
            {space.name}
          </span>
          <div class="ml-2 min-w-5 text-blue-700">
            {#if space.id === $currentSpace.id && !showSelectPrompt}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="2.5"
                stroke="currentColor"
                class="size-5"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            {/if}
          </div>
        </Button>
      {/if}
    {/each}
    <Button
      unstyled
      on:click={() => {
        $showCreateDialog = true;
      }}
      is={[$item]}
      class="mt-1 !justify-center rounded-lg border border-black/10 bg-blue-600 !py-2 text-white shadow-md hover:bg-blue-800  focus:outline-offset-4 focus:ring-offset-4"
      >Create a new space</Button
    >
    <div {...$arrow} use:arrow class="!z-10 border-black/35" />
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
