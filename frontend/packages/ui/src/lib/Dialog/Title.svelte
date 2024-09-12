<script lang="ts">
  import { Button } from "../Button/index.js";
  import { getDialog } from "./ctx.js";

  const {
    elements: { title, close }
  } = getDialog();
</script>

<div class="flex items-center justify-between pb-2">
  <h2 {...$title} use:title class="truncate text-xl font-medium">
    <slot />
  </h2>
  <Button is={[$close]} label="close" class="-mr-2" padding="icon"
    ><svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="h-6 w-6"
    >
      <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
    </svg>
  </Button>
</div>
