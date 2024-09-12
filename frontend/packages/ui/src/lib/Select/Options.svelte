<script lang="ts">
  import { getSelect } from "./ctx.js";

  const {
    elements: { menu }
  } = getSelect();
</script>

<div
  class=" z-10 flex flex-col gap-1 overflow-y-auto rounded-lg border border-stone-300 bg-white p-1 shadow-md shadow-stone-200 focus:!ring-0"
  {...$menu}
  use:menu
>
  <slot />
</div>
