<script lang="ts">
  import { getSelect } from "./ctx.js";

  const {
    elements: { menu }
  } = getSelect();
</script>

<div
  class=" z-10 flex flex-col gap-1 overflow-y-auto rounded-lg border border-stronger bg-primary p-1 shadow-md focus:!ring-0"
  {...$menu}
  use:menu
>
  <slot />
</div>
