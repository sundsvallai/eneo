<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { Button } from "@intric/ui";
  import { derived } from "svelte/store";
  import MemberChip from "./MemberChip.svelte";

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const members = derived(currentSpace, ($currentSpace) => {
    if ($currentSpace.members.length > 4) {
      const members = $currentSpace.members.slice(0, 3);
      return [
        ...members,
        {
          label: "+" + ($currentSpace.members.length - 3)
        }
      ];
    }
    return $currentSpace.members;
  });
</script>

<Button
  unstyled
  class="-mr-2 flex cursor-pointer rounded-lg p-2 pl-4 hover:bg-stone-200"
  href="/spaces/{$currentSpace.routeId}/members"
>
  {#each $members as member}
    <MemberChip {member}></MemberChip>
  {/each}
</Button>
