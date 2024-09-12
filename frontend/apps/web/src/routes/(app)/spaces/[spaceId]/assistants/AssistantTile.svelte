<script lang="ts">
  import type { AssistantSparse } from "@intric/intric-js";
  import AssistantActions from "./AssistantActions.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { getColourClass } from "$lib/core/colours";
  export let assistant: AssistantSparse;

  const {
    state: { currentSpace }
  } = getSpacesManager();
</script>

<a
  aria-label={assistant.name}
  href="/spaces/{$currentSpace.routeId}/assistants/{assistant.id}?tab=chat"
  class="relative flex flex-col items-start gap-2 p-2 px-4 {getColourClass(
    assistant.id
  )} group aspect-square border-t"
>
  <h2 class="line-clamp-2 pt-1 font-mono text-sm">
    {assistant.name}
  </h2>

  <div class="absolute bottom-2 right-2 hover:text-black">
    <AssistantActions {assistant}></AssistantActions>
  </div>

  <span
    class="pointer-events-none absolute inset-0 flex items-center justify-center font-mono text-[4.5rem] group-hover:text-white"
    >{[...assistant.name][0].toUpperCase()}</span
  >

  <div class="flex-grow"></div>
</a>

<style lang="postcss">
  .blue {
    @apply border-[#1e2466]  bg-[#1e246611] text-[#1e2466] hover:bg-[#1e2466] hover:text-white;
  }
  .green {
    @apply border-[#173026]  bg-[#17302611] text-[#173026] hover:bg-[#173026] hover:text-white;
  }
  .purple {
    @apply border-[#5e2dbf]  bg-[#5e2dbf11] text-[#5e2dbf] hover:bg-[#5e2dbf] hover:text-white;
  }
  .gold {
    @apply border-[#5c5b32]  bg-[#5c5b3211] text-[#5c5b32] hover:bg-[#5c5b32] hover:text-white;
  }
  .lightblue {
    @apply border-[#104dd0]  bg-[#104dd011] text-[#104dd0] hover:bg-[#104dd0] hover:text-white;
  }
  .white {
    @apply border-stone-800 text-center text-sm text-white;
  }
</style>
