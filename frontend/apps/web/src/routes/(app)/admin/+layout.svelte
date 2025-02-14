<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { dynamicColour } from "$lib/core/colours";
  import SpaceChip from "$lib/features/spaces/components/SpaceChip.svelte";
  import AdminMenu from "./AdminMenu.svelte";

  const { tenant } = getAppContext();
</script>

<div {...dynamicColour({ basedOn: "1" })} class="absolute inset-0 flex flex-grow justify-stretch">
  <div class="flex flex-col border-r-[0.5px] border-default md:min-w-[17rem] md:max-w-[17rem]">
    <div
      class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b-[0.5px] border-default pl-[1.4rem] pr-5 pt-0.5 font-medium"
    >
      <SpaceChip
        space={{
          id: "1",
          name: tenant.display_name ?? "Your organisation",
          personal: false
        }}
      ></SpaceChip>
      <span class="flex-grow truncate pl-0.5 text-left text-primary">
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
