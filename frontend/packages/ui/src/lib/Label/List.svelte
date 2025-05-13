<script lang="ts">
  import { default as Label, type LabelColor } from "./Single.svelte";

  export let content: { label: string | number; color: LabelColor; tooltip?: string }[];
  export let capitalize = true;
  export let monospaced = false;
</script>

<div class="flex flex-col py-2">
  {#if $$slots.default}
    <div class=" pl-0.5 font-medium"><slot /></div>
  {/if}
  <div class="flex flex-wrap items-center gap-1">
    {#each content as item (item)}
      <Label {item} {capitalize} {monospaced}></Label>
    {/each}
  </div>
</div>
