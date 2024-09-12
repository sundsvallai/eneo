<script lang="ts">
  import BlobPreview from "$lib/features/knowledge/components/BlobPreview.svelte";
  import LinkReference from "$lib/features/knowledge/components/LinkReference.svelte";
  import type { AssistantResponse } from "@intric/intric-js";

  export let message: Partial<AssistantResponse>;
  $: references = message.references?.slice(0, 3);
</script>

{#if references}
  <div
    class="-ml-2 flex flex-wrap gap-2 rounded-xl border-b border-stone-200/50 bg-gradient-to-b from-white to-stone-50 p-2 pr-4"
  >
    {#each references as reference}
      {#if reference.metadata.url}
        <LinkReference blob={reference} />
      {:else}
        <BlobPreview blob={reference} />
      {/if}
    {/each}
  </div>
{/if}
