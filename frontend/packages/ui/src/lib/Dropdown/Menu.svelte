<script lang="ts">
  import { getDropdown } from "./ctx.js";
  import { fly } from "svelte/transition";

  const {
    elements: { menu, item, arrow, overlay },
    states: { open }
  } = getDropdown();
</script>

{#if $open}
  <div {...$overlay} use:overlay class="fixed inset-0 z-[90]" />
  <div
    class="relative z-[100] min-w-[140px] rounded-md border border-black/20 bg-white shadow-md transition-all"
    {...$menu}
    use:menu
    transition:fly={{ duration: 150, y: -10 }}
  >
    <div class="relative z-20 flex flex-col items-stretch gap-1 rounded-md bg-white p-2">
      <slot item={[$item]} />
    </div>
    <div {...$arrow} use:arrow class="!z-10 border border-black/20" />
  </div>
{/if}
