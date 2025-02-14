<script lang="ts">
  import type { IntricInrefToken } from "../CustomComponents";
  import { getReferenceContext } from "../ReferenceContext.js";

  export let token: IntricInrefToken;

  const {
    state: { references },
    customComponent
  } = getReferenceContext();

  $: referenceIndex = $references.findIndex((ref) => ref.id.startsWith(token.id));
</script>

{#if customComponent}
  <svelte:component this={customComponent} id={token.id} references={$references}
  ></svelte:component>
{:else if referenceIndex > -1}
  <a
    class="reference"
    href={$references[referenceIndex].metadata.url}
    target="_blank"
    rel="noreferrer">{referenceIndex + 1}</a
  >
{/if}

<style lang="postcss">
  .reference {
    @apply inline-block min-h-7 min-w-7 rounded-lg border border-b-2 border-stronger bg-secondary px-2 text-center font-mono text-base font-normal no-underline hover:cursor-pointer hover:bg-hover-stronger;
  }
</style>
