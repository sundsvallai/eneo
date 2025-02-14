<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconSearch } from "@intric/icons/search";
  import { IconSelectedItem } from "@intric/icons/selected-item";
  import { Button, Dialog, Select } from "@intric/ui";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import type { SpaceRole, UserSparse } from "@intric/intric-js";
  import { createCombobox } from "@melt-ui/svelte";
  import MemberChip from "$lib/features/spaces/components/MemberChip.svelte";

  const intric = getIntric();
  const {
    refreshCurrentSpace,
    state: { currentSpace }
  } = getSpacesManager();

  export let allUsers: UserSparse[];
  export let currentMembers: UserSparse[];

  $: memberIds = currentMembers.map((member) => member.id);
  $: remainingUsers = allUsers.filter((user) => !memberIds.includes(user.id));

  let selectedRole: SpaceRole = $currentSpace.available_roles[0];

  const {
    elements: { menu, input, option },
    states: { open, inputValue, touchedInput, selected },
    helpers: { isSelected }
  } = createCombobox<UserSparse>({
    portal: null,
    positioning: {
      sameWidth: true,
      fitViewport: true,
      placement: "bottom"
    }
  });

  $: filteredUsers = $touchedInput
    ? remainingUsers.filter(({ email }) => email.toLowerCase().includes($inputValue.toLowerCase()))
    : remainingUsers;

  $: if (!$open) {
    $inputValue = $selected?.label ?? "";
  }

  async function addMember() {
    const id = $selected?.value.id;
    if (!id) return;
    isProcessing = true;
    try {
      await intric.spaces.members.add({
        spaceId: $currentSpace.id,
        user: { id, role: selectedRole.value }
      });
      refreshCurrentSpace();
      $showDialog = false;
      $selected = undefined;
    } catch (e) {
      alert("Could not add new member.");
      console.error(e);
    }
    isProcessing = false;
  }

  let inputElement: HTMLInputElement;
  let isProcessing = false;
  let showDialog: Dialog.OpenState;
</script>

<Dialog.Root bind:isOpen={showDialog}>
  <Dialog.Trigger asFragment let:trigger>
    <Button variant="primary" is={trigger}>Add new member</Button>
  </Dialog.Trigger>

  <Dialog.Content width="medium" form>
    <Dialog.Title>Add new member</Dialog.Title>

    <Dialog.Section scrollable={false}>
      <div class="flex items-center rounded-md hover:bg-hover-dimmer">
        <div class="flex flex-grow flex-col gap-1 rounded-md pb-4 pl-4 pr-2 pt-2">
          <div>
            <span class="pl-3 font-medium">User</span>
          </div>

          <div class="relative flex flex-grow">
            <input
              bind:this={inputElement}
              placeholder="Find user..."
              {...$input}
              required
              use:input
              class="relative h-10 w-full items-center justify-between overflow-hidden rounded-lg
            border border-stronger bg-primary px-3 py-2 shadow ring-default placeholder:text-secondary focus-within:ring-2 hover:ring-2 focus-visible:ring-2 disabled:bg-secondary disabled:text-muted disabled:shadow-none disabled:hover:ring-0"
            />
            <button
              on:click={() => {
                inputElement.focus();
                $open = true;
              }}
            >
              <IconSearch class="absolute right-4 top-2" />
            </button>
          </div>
          <ul
            class="shadow-bg-secondary relative z-10 flex flex-col gap-1 overflow-y-auto rounded-lg border border-stronger bg-primary p-1 shadow-md focus:!ring-0"
            {...$menu}
            use:menu
          >
            <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
            <div class="flex flex-col gap-0 bg-primary text-primary" tabindex="0">
              {#each filteredUsers as user, index (index)}
                <li
                  {...$option({
                    value: user,
                    label: user.email
                  })}
                  use:option
                  class="flex items-center gap-1 rounded-md px-2 py-1 hover:cursor-pointer hover:bg-hover-default"
                >
                  <IconSelectedItem
                    class="{$isSelected(user) ? 'block' : 'hidden'} text-accent-default"
                  />
                  <div class="px-2">
                    <MemberChip member={user}></MemberChip>
                  </div>

                  <span class="flex w-full items-center justify-between truncate py-1 text-primary">
                    {user.email}
                  </span>
                </li>
              {/each}
            </div>
          </ul>
        </div>
        <Select.Simple
          fitViewport={true}
          class="w-1/3  p-4 pl-2 "
          options={$currentSpace.available_roles.map((role) => {
            return { label: role.label, value: role };
          })}
          bind:value={selectedRole}>Role</Select.Simple
        >
      </div>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>

      <Button variant="primary" on:click={addMember} type="submit"
        >{isProcessing ? "Adding..." : "Add member"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<style lang="postcss">
  li[data-disabled] {
    @apply pointer-events-none !cursor-not-allowed opacity-30 hover:bg-transparent;
  }
</style>
