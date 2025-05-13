<script lang="ts">
  import { getDropdown } from "./ctx.js";
  import { fly } from "svelte/transition";

  const {
    elements: { menu, item, arrow, overlay },
    states: { open }
  } = getDropdown();
</script>

{#if $open}
  <div {...$overlay} use:overlay class="fixed inset-0 z-[90]"></div>
  <div
    class=" border-default bg-primary relative z-[100] min-w-[140px] rounded-md border shadow-lg transition-all"
    {...$menu}
    use:menu
    transition:fly={{ duration: 150, y: -10 }}
  >
    <div class="bg-primary relative z-20 flex flex-col items-stretch gap-1 rounded-md p-2">
      <slot item={[$item]} />
    </div>
    <div {...$arrow} use:arrow class="border-default !z-10 border"></div>
  </div>
{/if}
