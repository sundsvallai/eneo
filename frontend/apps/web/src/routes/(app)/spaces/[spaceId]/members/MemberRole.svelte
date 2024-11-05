<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import type { UserSparse } from "@intric/intric-js";
  import { Button, Dialog } from "@intric/ui";
  import { createSelect } from "@melt-ui/svelte";

  type SpaceRole = "admin" | "editor";

  export let member: UserSparse & { role: SpaceRole };
  const intric = getIntric();
  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  const options = [{ value: "admin" }, { value: "editor" }, { value: "remove" }];

  const {
    elements: { trigger, menu, option, label },
    states: { selected },
    helpers: { isSelected }
  } = createSelect<SpaceRole | "remove">({
    positioning: {
      placement: "bottom",
      fitViewport: true,
      sameWidth: false
    },
    defaultSelected: { value: member.role },
    onSelectedChange: ({ curr, next }) => {
      if (!next) return curr;
      if (next.value === "remove") {
        $showRemoveDialog = true;
        return curr;
      }
      changeRole(next.value);
      return next;
    }
  });

  let isRemoving = false;
  async function removeMember() {
    isRemoving = true;
    try {
      await intric.spaces.members.remove({ spaceId: $currentSpace.id, user: member });
      await refreshCurrentSpace();
    } catch (e) {
      alert("Couldn't remove user.");
      console.error(e);
    }
    isRemoving = false;
    $showRemoveDialog = false;
  }

  async function changeRole(newRole: SpaceRole) {
    if (member.role !== newRole) {
      try {
        await intric.spaces.members.update({
          spaceId: $currentSpace.id,
          user: { id: member.id, role: newRole }
        });
        refreshCurrentSpace();
      } catch (e) {
        alert("Couldn't change role.");
        console.error(e);
        $selected = { value: member.role };
      }
    }
  }

  let showRemoveDialog: Dialog.OpenState;
</script>

<div class="relative flex flex-col gap-1">
  <!-- svelte-ignore a11y-label-has-associated-control -->
  <label class="sr-only pl-3 font-medium" {...$label} use:label>
    Select a role for this member
  </label>

  <Button is={[$trigger]}>
    <div class="truncate capitalize">
      {$selected?.value}
    </div>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="h-6 w-6"
    >
      <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
    </svg>
  </Button>

  <div
    class=" z-10 flex flex-col gap-1 overflow-y-auto rounded-lg border border-stone-300 bg-white p-1 shadow-md shadow-stone-200 focus:!ring-0"
    {...$menu}
    use:menu
  >
    {#each options as item}
      <div
        class="flex items-center gap-1 rounded-md hover:cursor-pointer hover:bg-stone-200"
        {...$option({ value: item.value })}
        use:option
      >
        <div class="px-3 py-1 capitalize" class:destructive={item.value === "remove"}>
          {item.value}
        </div>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="2.5"
          stroke="currentColor"
          class="h-5 w-5 {$isSelected(item.value) ? 'block' : 'hidden'} mr-3 text-blue-600"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
        </svg>
      </div>
    {/each}
  </div>
</div>

<Dialog.Root alert bind:isOpen={showRemoveDialog}>
  <Dialog.Content>
    <Dialog.Title>Remove member</Dialog.Title>
    <Dialog.Description
      >Do you really want to remove <span class="italic">{member.username}</span> from this space?</Dialog.Description
    >
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={removeMember}>{isRemoving ? "Removing..." : "Remove"}</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<style lang="postcss">
  div[data-highlighted] {
    @apply bg-stone-200;
  }

  div[data-disabled] {
    @apply opacity-30 hover:bg-transparent;
  }

  .destructive {
    @apply w-full rounded-md border border-red-500 text-red-500 hover:bg-red-500 hover:text-white;
  }
</style>
