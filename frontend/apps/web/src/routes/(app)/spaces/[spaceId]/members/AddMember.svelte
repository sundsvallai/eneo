<!-- MIT License -->

<script lang="ts">
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import type { UserSparse } from "@intric/intric-js";
  import { Button, Dialog, Select } from "@intric/ui";
  import { createCombobox } from "@melt-ui/svelte";
  import MemberChip from "./MemberChip.svelte";

  const intric = getIntric();
  const {
    refreshCurrentSpace,
    state: { currentSpace }
  } = getSpacesManager();

  export let allUsers: UserSparse[];
  export let currentMembers: UserSparse[];

  $: memberIds = currentMembers.map((member) => member.id);
  $: remainingUsers = allUsers.filter((user) => !memberIds.includes(user.id));

  let selectedRole: "admin" | "editor" = "editor";

  const {
    elements: { menu, input, option },
    states: { open, inputValue, touchedInput, selected },
    helpers: { isSelected }
  } = createCombobox<UserSparse>({
    portal: null,
    positioning: {
      sameWidth: true,
      fitViewport: false,

      placement: "bottom"
    }
  });

  $: filteredUsers = $touchedInput
    ? remainingUsers.filter(
        ({ username, email }) =>
          username.toLowerCase().includes($inputValue.toLowerCase()) ||
          email.toLowerCase().includes($inputValue.toLowerCase())
      )
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
        user: { id, role: selectedRole }
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

  <Dialog.Content wide form>
    <Dialog.Title>Add new member</Dialog.Title>

    <Dialog.Section scrollable={false}>
      <div class="flex items-center rounded-md hover:bg-stone-50">
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
            border border-stone-300 bg-white px-3 py-2 shadow ring-stone-200 placeholder:text-stone-400 focus-within:ring-2 hover:ring-2 focus-visible:ring-2 disabled:bg-stone-50 disabled:text-stone-500 disabled:shadow-none disabled:hover:ring-0"
            />
            <button
              on:click={() => {
                inputElement.focus();
                $open = true;
              }}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="absolute right-4 top-2 h-6 w-6"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
                />
              </svg>
            </button>
          </div>
          <ul
            class="relative z-10 flex flex-col gap-1 overflow-y-auto rounded-lg border border-stone-300 bg-white p-1 shadow-md shadow-stone-200 focus:!ring-0"
            {...$menu}
            use:menu
          >
            <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
            <div class="flex flex-col gap-0 bg-white text-black" tabindex="0">
              {#each filteredUsers as user, index (index)}
                <li
                  {...$option({
                    value: user,
                    label: user.username
                  })}
                  use:option
                  class="flex items-center gap-1 rounded-md px-2 py-1 hover:cursor-pointer hover:bg-stone-200"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="2.5"
                    stroke="currentColor"
                    class="h-5 w-5 {$isSelected(user) ? 'block' : 'hidden'} text-blue-600"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="m4.5 12.75 6 6 9-13.5"
                    />
                  </svg>

                  <div class="pl-2">
                    <MemberChip member={user}></MemberChip>
                  </div>

                  <div class="flex w-full items-center justify-between py-1">
                    <span>
                      {user.username}
                    </span>
                    <span class="font-mono text-sm text-stone-400">{user.email}</span>
                  </div>
                </li>
              {/each}
            </div>
          </ul>
        </div>
        <Select.Simple
          fitViewport={false}
          class="w-1/3  p-4 pl-2 "
          options={[
            { value: "editor", label: "Editor" },
            { value: "admin", label: "Admin" }
          ]}
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
