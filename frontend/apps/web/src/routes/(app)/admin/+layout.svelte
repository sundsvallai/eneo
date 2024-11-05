<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { getColourClass } from "$lib/core/colours";
  import SpaceChip from "$lib/features/spaces/components/SpaceChip.svelte";
  import AdminMenu from "./AdminMenu.svelte";

  const { tenant } = getAppContext();
</script>

<div class="absolute inset-0 flex flex-grow justify-stretch {getColourClass('1')}">
  <div class="flex flex-col border-r-[0.5px] border-black/10 md:min-w-[17rem] md:max-w-[17rem]">
    <div
      class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b-[0.5px] border-black/15 pl-[1.4rem] pr-5 pt-0.5 font-medium"
    >
      <SpaceChip
        space={{
          id: "1",
          name: tenant.display_name ?? "Your organisation",
          personal: false
        }}
      ></SpaceChip>
      <span class="flex-grow truncate pl-0.5 text-left">
        {tenant.display_name ?? "Your organisation"}
      </span>
    </div>
    <AdminMenu></AdminMenu>
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
