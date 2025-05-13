<script lang="ts">
  import { createDropdown } from "./ctx.js";

  export let placement: "bottom" | "bottom-start" | "bottom-end" | undefined = undefined;
  export let arrowSize: number | undefined = undefined;
  export let gutter: number | undefined = undefined;

  const {
    states: { open }
  } = createDropdown(placement, arrowSize, gutter);
</script>

<div class="relative">
  <slot {open} />
</div>
