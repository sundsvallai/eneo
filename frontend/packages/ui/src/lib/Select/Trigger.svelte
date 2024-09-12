<script lang="ts">
  import { getSelect } from "./ctx.js";

  export let placeholder = "select";
  export let error = false;

  const {
    elements: { trigger },
    states: { selectedLabel }
  } = getSelect();
</script>

<button
  class="flex h-10 items-center justify-between
overflow-hidden rounded-lg border {error
    ? 'border-2 border-red-500'
    : 'border-stone-300'} bg-white px-3 py-2 shadow ring-stone-200 focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
  {...$trigger}
  use:trigger
>
  <div class="truncate">
    {$selectedLabel || placeholder}
  </div>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="1.5"
    stroke="currentColor"
    class="h-6 w-6"
  >
    <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
  </svg>
</button>
