<script lang="ts">
  import { getSelect } from "./ctx.js";

  const {
    elements: { label }
  } = getSelect();
</script>

<label class="pl-3 font-medium" {...$label} use:label>
  <slot />
</label>
