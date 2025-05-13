<script lang="ts">
  import { dynamicColour } from "$lib/core/colours";

  export let app: { id: string; name: string };
  export let size: "medium" | "large" = "large";
</script>

<div
  {...dynamicColour({ basedOn: app.id })}
  class="{size} app-icon border-dynamic-default text-dynamic-stronger pointer-events-none rounded-[2rem] border"
>
  <div class="flex items-center justify-center bg-[var(--dynamic-transparent)] font-mono font-bold">
    {[...app.name][0]}
  </div>
</div>

<style lang="postcss">
  @reference "@intric/ui/styles";
  div {
    --dynamic-transparent: oklch(from var(--dynamic-default) l c h / 8%);
  }
  .large {
    @apply rounded-[2rem] border-b-4 p-2;
  }
  .large div {
    @apply min-h-24 min-w-24 rounded-[1.5rem] text-[2.6rem];
  }
  .medium {
    @apply rounded-[0.9rem] border-b-4 p-1;
  }
  .medium div {
    @apply min-h-12 min-w-12 rounded-[0.7rem] text-[1.8rem];
  }
  .app-icon {
    box-shadow:
      0px 8px 30px -5px rgb(from var(--dynamic-default) r g b / 20%),
      0px 8px 20px -10px rgb(from var(--dynamic-default) r g b / 50%);
    background: linear-gradient(
      0deg,
      var(--background-primary) 0%,
      var(--dynamic-transparent) 100%
    );
  }
</style>
