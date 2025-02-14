<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import type { SpaceSparse } from "@intric/intric-js";
  import { dynamicColour } from "$lib/core/colours";
  export let space: SpaceSparse;
</script>

<a
  aria-label={space.name}
  href="/spaces/{space.id}"
  {...dynamicColour({ basedOn: space.id })}
  class="group relative flex aspect-square flex-col items-start gap-4 border-t border-dynamic-default bg-dynamic-dimmer p-4 pt-2 text-dynamic-stronger hover:bg-dynamic-default hover:text-on-fill"
>
  <h2 class="line-clamp-3 pt-1 font-mono text-sm">
    {space.name}
  </h2>

  <div class="pointer-events-none absolute inset-0 flex items-center justify-center">
    <span
      class="flex aspect-square h-20 items-center justify-center rounded-xl border border-transparent bg-dynamic-default font-sans text-[3rem] text-on-fill group-hover:border-on-fill"
      >{[...space.name][0].toUpperCase()}</span
    >
  </div>

  <div class="pointer-events-none absolute inset-0 flex items-center justify-center"></div>
</a>
