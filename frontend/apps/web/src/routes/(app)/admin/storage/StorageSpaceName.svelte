<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import SpaceChip from "$lib/features/spaces/components/SpaceChip.svelte";
  import type { StorageSpaceInfo } from "@intric/intric-js";

  export let space: StorageSpaceInfo;
</script>

<div class="flex w-full items-center justify-start gap-2">
  <SpaceChip space={{ ...space, personal: false }}></SpaceChip>

  <span class="truncate overflow-ellipsis text-primary">
    {space.name}
  </span>
</div>
