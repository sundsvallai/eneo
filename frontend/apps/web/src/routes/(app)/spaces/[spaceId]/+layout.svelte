<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { getColourClass } from "$lib/core/colours";
  import SpaceSelector from "$lib/features/spaces/components/SpaceSelector.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager.js";
  import SpaceMenu from "./SpaceMenu.svelte";

  export let data;

  // Hint: SpacesManager will listen to route / spaceId changes
  const {
    state: { currentSpace },
    watchPageData
  } = getSpacesManager();

  const { user } = getAppContext();

  $: watchPageData(data);
</script>

<svelte:head>
  <title>intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name}</title>
</svelte:head>

<div
  class="absolute inset-0 flex flex-grow justify-stretch {getColourClass(
    $currentSpace.personal ? user.id : $currentSpace.id
  )}"
>
  <div class="flex flex-col border-r-[0.5px] border-black/10 md:min-w-[17rem] md:max-w-[17rem]">
    <SpaceSelector></SpaceSelector>
    <SpaceMenu></SpaceMenu>
  </div>
  <slot />
  <div
    class="pointer-events-none absolute inset-0 -z-0 flex flex-grow shadow-xl md:left-[17rem]"
  ></div>
</div>

<style>
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
