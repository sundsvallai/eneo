<script lang="ts">
  import type { AssistantResponse } from "@intric/intric-js";
  import { IconCopy } from "@intric/icons/copy";
  import { IconChevronRight } from "@intric/icons/chevron-right";
  import { Button, Tooltip } from "@intric/ui";
  import BlobPreview from "$lib/features/knowledge/components/BlobPreview.svelte";
  import LinkReference from "$lib/features/knowledge/components/LinkReference.svelte";

  export let message: AssistantResponse;
  export let isLast: boolean;

  let referencesExpanded = false;

  let showCopiedMessage = false;
</script>

<div
  class:showOnHover={true}
  class:md:opacity-0={!referencesExpanded && !isLast}
  class="mb-6 flex flex-col items-start group-hover/message:opacity-100 md:-mb-2"
>
  <div class="flex gap-2">
    <Tooltip text="Copy response">
      <Button
        on:click={() => {
          navigator.clipboard.writeText(message.answer);
          showCopiedMessage = true;
          setTimeout(() => {
            showCopiedMessage = false;
          }, 2000);
        }}
        unstyled
        class="flex gap-2 rounded-lg border border-default p-1.5 shadow-sm hover:bg-hover-stronger"
        padding="icon"
        ><IconCopy />
        {#if showCopiedMessage}
          <span class="pr-2">Copied!</span>
        {/if}
      </Button>
    </Tooltip>

    {#if message.references.length > 0}
      <Button
        unstyled
        class="flex gap-1 rounded-lg border border-default p-1.5 pr-2.5 shadow-sm hover:bg-hover-dimmer"
        on:click={() => {
          referencesExpanded = !referencesExpanded;
        }}
      >
        <IconChevronRight
          class={referencesExpanded ? "rotate-90 transition-all" : "transition-all"}
        />
        {message.references.length} references
      </Button>
    {/if}
  </div>
  {#if referencesExpanded}
    <div class="mb-2 flex w-full flex-wrap gap-2 pt-2 md:pb-6">
      {#each message.references as reference, index}
        {#if reference.metadata.url}
          <LinkReference blob={reference} index={index + 1} />
        {:else}
          <BlobPreview blob={reference} index={index + 1} />
        {/if}
      {/each}
    </div>
  {/if}
</div>
