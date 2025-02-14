<script lang="ts">
  import type { AssistantSparse } from "@intric/intric-js";
  import AssistantActions from "./AssistantActions.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { dynamicColour } from "$lib/core/colours";
  export let assistant: AssistantSparse;

  const {
    state: { currentSpace }
  } = getSpacesManager();
</script>

<a
  aria-label={assistant.name}
  {...dynamicColour({ basedOn: assistant.id })}
  href="/spaces/{$currentSpace.routeId}/assistants/{assistant.id}?tab=chat"
  class="group relative flex aspect-square flex-col items-start gap-2 border-t border-dynamic-default bg-dynamic-dimmer p-2 px-4 text-dynamic-stronger hover:bg-dynamic-default hover:text-on-fill"
>
  <h2 class="line-clamp-2 pt-1 font-mono text-sm">
    {assistant.name}
  </h2>

  <div class="absolute bottom-2 right-2 hover:text-primary">
    <AssistantActions {assistant}></AssistantActions>
  </div>

  <span
    class="pointer-events-none absolute inset-0 flex items-center justify-center font-mono text-[4.5rem] group-hover:text-on-fill"
    >{([...assistant.name][0] ?? "").toUpperCase()}</span
  >

  <div class="flex-grow"></div>
</a>
