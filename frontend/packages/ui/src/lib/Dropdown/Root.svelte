<script lang="ts">
  import { createDropdown } from "./ctx.js";

  const {
    states: { open }
  } = createDropdown();
</script>

<div class="relative">
  <slot {open} />
</div>
