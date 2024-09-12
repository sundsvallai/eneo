<script context="module" lang="ts">
  export type LabelColor = "blue" | "green" | "yellow" | "orange" | "gray" | "gold";
</script>

<script lang="ts">
  import Tooltip from "$lib/Tooltip/Root.svelte";
  export let item: { label: string | number; color: LabelColor; tooltip?: string };
  export let capitalize = true;
  export let monospaced = false;
</script>

{#if item.tooltip}
  <Tooltip text={item.tooltip} asFragment let:trigger>
    {@const tooltipTrigger = trigger[0]}
    <div
      {...tooltipTrigger}
      use:tooltipTrigger.action
      class:capitalize
      class:font-mono={monospaced}
      class={`${item.color} inline-block cursor-default rounded-md border px-2 py-1  text-sm `}
    >
      {item.label}
    </div>
  </Tooltip>
{:else}
  <div
    class:capitalize
    class:font-mono={monospaced}
    class={`${item.color} inline-block cursor-default rounded-md border px-2 py-1  text-sm `}
  >
    {item.label}
  </div>
{/if}

<style lang="postcss">
  .blue {
    @apply border-blue-600 bg-blue-50 text-blue-700;
  }
  .green {
    @apply border-green-600 bg-green-50 text-green-700;
  }
  .yellow {
    @apply border-yellow-600 bg-yellow-50 text-yellow-700;
  }
  .orange {
    @apply border-orange-600 bg-orange-50 text-orange-700;
  }
  .gray {
    @apply border-stone-500 bg-stone-50 text-stone-500;
  }
  .gold {
    @apply border-[#5c5b32] bg-[#5c5b3211] text-[#5c5b32];
  }
</style>
