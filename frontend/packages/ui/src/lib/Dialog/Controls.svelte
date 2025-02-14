<script lang="ts">
  import { getDialog } from "./ctx.js";

  const {
    elements: { close }
  } = getDialog();
</script>

<div class="flex w-full items-center justify-end gap-2 py-2">
  <slot close={[$close]} />
</div>
