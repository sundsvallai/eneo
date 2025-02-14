<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { dynamicColour } from "$lib/core/colours";
  import type { AppSparse } from "@intric/intric-js";
  import AppIcon from "$lib/features/apps/components/AppIcon.svelte";
  import AppActions from "./AppActions.svelte";

  export let app: AppSparse;

  const {
    state: { currentSpace }
  } = getSpacesManager();
</script>

<a
  aria-label={app.name}
  {...dynamicColour({ basedOn: app.id })}
  href="/spaces/{$currentSpace.routeId}/apps/{app.id}"
  class="group relative flex aspect-square flex-col items-start gap-2 border-t border-dynamic-default bg-dynamic-dimmer p-2 px-4 text-dynamic-stronger hover:bg-dynamic-default hover:text-on-fill"
>
  <h2 class="line-clamp-2 pt-1 font-mono text-sm">
    {app.name}
  </h2>

  <div class="absolute bottom-2 right-2 hover:text-primary">
    <AppActions {app}></AppActions>
  </div>

  <span
    class="pointer-events-none absolute inset-0 flex items-center justify-center font-mono text-[4.5rem] group-hover:text-on-fill"
  >
    <AppIcon {app}></AppIcon>
  </span>

  <div class="flex-grow"></div>
</a>
