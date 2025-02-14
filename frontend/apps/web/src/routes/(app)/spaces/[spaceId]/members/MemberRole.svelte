<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconChevronDown } from "@intric/icons/chevron-down";
  import { IconSelectedItem } from "@intric/icons/selected-item";
  import { Button, Dialog } from "@intric/ui";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import type { Space, SpaceRole } from "@intric/intric-js";
  import { createSelect } from "@melt-ui/svelte";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";

  type Member = Space["members"]["items"][number];
  type RoleOption = { label: string; value: SpaceRole["value"] | "remove" };

  export let member: Member;
  const intric = getIntric();

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  const options: RoleOption[] = [
    ...$currentSpace.available_roles,
    { label: "Remove", value: "remove" }
  ];

  const {
    elements: { trigger, menu, option, label },
    states: { selected },
    helpers: { isSelected }
  } = createSelect({
    positioning: {
      placement: "bottom",
      fitViewport: true,
      sameWidth: false
    },
    defaultSelected: { value: member.role }
  });

  $: $selected = { value: member.role };

  let isRemoving = false;
  async function removeMember() {
    isRemoving = true;
    try {
      await intric.spaces.members.remove({ spaceId: $currentSpace.id, user: member });
      // Will cause an update in the parent page
      await refreshCurrentSpace();
    } catch (e) {
      alert("Couldn't remove user.");
      console.error(e);
    }
    isRemoving = false;
    $showRemoveDialog = false;
  }

  async function changeRole(newRole: RoleOption) {
    if (newRole.value === "remove") {
      $showRemoveDialog = true;
      return;
    }
    if (member.role !== newRole.value) {
      try {
        isLoading = true;
        await intric.spaces.members.update({
          spaceId: $currentSpace.id,
          user: { id: member.id, role: newRole.value }
        });
        refreshCurrentSpace();
      } catch (e) {
        isLoading = false;
        alert("Couldn't change role.");
        console.error(e);
        $selected = { value: member.role };
      }
    }
  }

  let showRemoveDialog: Dialog.OpenState;

  let isLoading = false;
  $: resetLoading(member);
  function resetLoading(member: Member) {
    if (member) {
      isLoading = false;
    }
  }
</script>

<div class="relative flex flex-col gap-1">
  <!-- svelte-ignore a11y-label-has-associated-control -->
  <label class="sr-only pl-3 font-medium" {...$label} use:label>
    Select a role for this member
  </label>

  <Button is={[$trigger]}>
    <div class="truncate capitalize">
      {#if isLoading}
        <IconLoadingSpinner class="animate-spin"></IconLoadingSpinner>
      {:else}
        {member.role}
      {/if}
    </div>
    <IconChevronDown />
  </Button>

  <div
    class="z-10 flex flex-col gap-1 overflow-y-auto rounded-lg border border-stronger bg-primary p-1 shadow-md focus:!ring-0"
    {...$menu}
    use:menu
  >
    {#each options as item}
      <div
        class="flex items-center gap-1 rounded-md text-primary hover:cursor-pointer hover:bg-hover-default"
        {...$option({ value: item.value })}
        use:option
      >
        <Button
          class="w-full !justify-start capitalize"
          variant={item.value === "remove" ? "destructive" : "simple"}
          on:click={() => {
            changeRole(item);
          }}
        >
          <span>
            {item.value}
          </span>
          {#if $isSelected(item.value)}
            <IconSelectedItem class="text-accent-default" />
          {/if}
        </Button>
      </div>
    {/each}
  </div>
</div>

<Dialog.Root alert bind:isOpen={showRemoveDialog}>
  <Dialog.Content width="small">
    <Dialog.Title>Remove member</Dialog.Title>
    <Dialog.Description
      >Do you really want to remove <span class="italic">{member.email}</span> from this space?</Dialog.Description
    >
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="destructive" on:click={removeMember}
        >{isRemoving ? "Removing..." : "Remove"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<style lang="postcss">
  div[data-highlighted] {
    @apply bg-secondary;
  }

  div[data-disabled] {
    @apply opacity-30 hover:bg-transparent;
  }
</style>
