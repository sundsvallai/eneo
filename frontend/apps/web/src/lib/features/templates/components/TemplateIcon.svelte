<script lang="ts">
  import { dynamicColour } from "$lib/core/colours";

  export let template: { name: string; category: string };
  export let size: "medium" | "large" = "medium";
</script>

<div
  {...dynamicColour({ basedOn: template.category })}
  class="flex items-center justify-center rounded-lg border border-dynamic-stronger bg-dynamic-dimmer {size}"
>
  <span class=" text-dynamic-stronger">{[...template.name][0]}</span>
</div>

<style lang="postcss">
  .medium {
    @apply h-7 w-7 min-w-7 text-lg font-medium;
  }
  .large {
    @apply h-9 w-9 min-w-9 text-2xl font-extrabold;
  }
</style>
