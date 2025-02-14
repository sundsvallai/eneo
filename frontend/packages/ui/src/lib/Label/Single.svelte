<script context="module" lang="ts">
  export type LabelColor = "blue" | "green" | "yellow" | "orange" | "gray" | "gold";
</script>

<script lang="ts">
  import Tooltip from "$lib/Tooltip/Root.svelte";
  export let item: { label: string | number; color: LabelColor; tooltip?: string };
  export let capitalize = true;
  export let monospaced = false;

  // Temporary fix for the color mapping to new classnames
  const colorMap: Record<LabelColor, string> = {
    blue: "label-blue",
    green: "label-green",
    yellow: "label-yellow",
    orange: "label-yellow",
    gray: "label-grey",
    gold: "label-grey"
  };
</script>

{#if item.tooltip}
  <Tooltip text={item.tooltip} asFragment let:trigger>
    {@const tooltipTrigger = trigger[0]}
    <div
      {...tooltipTrigger}
      use:tooltipTrigger.action
      class:capitalize
      class:font-mono={monospaced}
      class="{colorMap[
        item.color
      ]} inline-block cursor-default rounded-md border border-label-default bg-label-dimmer px-2 py-1 text-sm text-label-stronger"
    >
      {item.label}
    </div>
  </Tooltip>
{:else}
  <div
    class:capitalize
    class:font-mono={monospaced}
    class="{colorMap[
      item.color
    ]} inline-block cursor-default rounded-md border border-label-default bg-label-dimmer px-2 py-1 text-sm text-label-stronger"
  >
    {item.label}
  </div>
{/if}
