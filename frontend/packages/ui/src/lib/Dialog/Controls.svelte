<script lang="ts">
  import { getDialog } from "./ctx.js";

  const {
    elements: { close }
  } = getDialog();
</script>

<div class="flex w-full translate-x-0.5 translate-y-0.5 items-center justify-end gap-2 pt-3">
  <slot close={[$close]} />
</div>
