<script lang="ts">
  import { getSelect } from "./ctx.js";

  export let value: unknown;
  export let label: string;
  export let disabled = false;

  const {
    elements: { option },
    helpers: { isSelected }
  } = getSelect();
</script>

<div
  class="bg-primary text-primary data-[highlighted]:bg-hover-default flex items-center gap-1 rounded-md px-2 hover:cursor-pointer data-[disabled]:opacity-30 data-[disabled]:hover:bg-transparent"
  {...$option({ value, label, disabled })}
  use:option
>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="2.5"
    stroke="currentColor"
    class="h-5 w-5 {$isSelected(value) ? 'block' : 'hidden'} text-accent-default"
  >
    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
  </svg>
  {#if $$slots.default}
    <slot />
  {:else}
    <div class="py-1">
      {label}
    </div>
  {/if}
</div>
