<script lang="ts">
  import type { ServiceSparse } from "@intric/intric-js";
  import { IconService } from "@intric/icons/service";
  import ServiceActions from "./ServiceActions.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { dynamicColour } from "$lib/core/colours";

  export let service: ServiceSparse;

  const {
    state: { currentSpace }
  } = getSpacesManager();
</script>

<a
  aria-label={service.name}
  {...dynamicColour({ basedOn: service.id })}
  href="/spaces/{$currentSpace.routeId}/services/{service.id}?tab=playground"
  class="group relative flex aspect-square flex-col items-start gap-2 border-t border-dynamic-default bg-dynamic-dimmer p-2 px-4 text-dynamic-stronger hover:bg-dynamic-default hover:text-on-fill"
>
  <h2 class="line-clamp-2 pt-1 font-mono text-sm">
    {service.name}
  </h2>

  <div class="absolute bottom-2 right-2 hover:text-primary">
    <ServiceActions {service}></ServiceActions>
  </div>

  <span
    class="pointer-events-none absolute inset-0 flex items-center justify-center font-mono text-[4.5rem] group-hover:text-on-fill"
  >
    <IconService size="lg" />
  </span>

  <div class="flex-grow"></div>
</a>
