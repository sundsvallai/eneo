<script lang="ts">
  import BlobPreview from "$lib/features/knowledge/components/BlobPreview.svelte";
  import type { InfoBlob } from "@intric/intric-js";
  import { Tooltip } from "@intric/ui";

  export let id: string;
  export let references: InfoBlob[];

  $: refIndex = references.findIndex((ref) => ref.id.startsWith(id));
</script>

{#if refIndex > -1}
  {@const reference = references[refIndex]}
  {#if reference.metadata.url}
    <Tooltip text={reference.metadata.url} renderInline>
      <a href={reference.metadata.url} target="_blank" rel="noreferrer">
        {refIndex + 1}
      </a>
    </Tooltip>
  {:else}
    <Tooltip text={reference.metadata.title ?? undefined} renderInline>
      <BlobPreview let:showBlob blob={reference}>
        <button on:click={showBlob}>{refIndex + 1}</button>
      </BlobPreview>
    </Tooltip>
  {/if}
{/if}

<style lang="postcss">
  button,
  a {
    @apply inline-block min-h-7 min-w-7 rounded-lg border border-b-2 border-default bg-secondary px-2 text-center font-mono text-base font-normal no-underline shadow hover:cursor-pointer hover:bg-hover-stronger;
  }
</style>
