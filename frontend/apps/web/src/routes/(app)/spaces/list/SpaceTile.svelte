<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import type { SpaceSparse } from "@intric/intric-js";
  import { getColourClass } from "$lib/core/colours";
  export let space: SpaceSparse;
</script>

<a
  aria-label={space.name}
  href="/spaces/{space.id}"
  class="relative flex items-start gap-4 p-4 pt-2 {getColourClass(
    space.id
  )} group aspect-square flex-col border-t border-[var(--space-color)] bg-[var(--space-color-light)] text-[var(--space-color)] hover:bg-[var(--space-color)] hover:text-white"
>
  <h2 class="line-clamp-3 pt-1 font-mono text-sm">
    {space.name}
  </h2>

  <div class="pointer-events-none absolute inset-0 flex items-center justify-center">
    <span
      class="flex aspect-square h-20 items-center justify-center rounded-xl border border-transparent bg-[var(--space-color)] font-sans text-[3rem] text-white/80 group-hover:border-stone-50/50"
      >{[...space.name][0].toUpperCase()}</span
    >
  </div>

  <div class="pointer-events-none absolute inset-0 flex items-center justify-center"></div>
</a>

<style lang="postcss">
  .blue {
    --space-color: #1e2466;
    --space-color-light: #1e246611;
  }
  .green {
    --space-color: #173026;
    --space-color-light: #17302611;
  }
  .purple {
    --space-color: #5e2dbf;
    --space-color-light: #5e2dbf11;
  }
  .gold {
    --space-color: #5c5b32;
    --space-color-light: #5c5b3211;
  }
  .lightblue {
    --space-color: #104dd0;
    --space-color-light: #104dd011;
  }
</style>
