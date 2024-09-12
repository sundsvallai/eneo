<script lang="ts">
  import { getDialog } from "./ctx.js";

  export let hidden = false;

  const {
    elements: { description }
  } = getDialog();
</script>

<p {...$description} use:description class:hidden>
  <slot />
</p>
