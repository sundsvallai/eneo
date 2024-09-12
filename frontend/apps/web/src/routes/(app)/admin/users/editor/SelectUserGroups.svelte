<!-- MIT License -->

<script lang="ts">
  import { getIntric } from "$lib/core/Intric";
  import type { UserGroup } from "@intric/intric-js";
  import { Button } from "@intric/ui";
  import { createCombobox } from "@melt-ui/svelte";

  // Array of all currently selected collections
  export let selectedGroups: UserGroup[];
  export let userGroups: UserGroup[];
  export let user: { id: string };

  const intric = getIntric();

  const {
    elements: { menu, input, option },
    states: { open, inputValue, touchedInput, selected },
    helpers: { isSelected }
  } = createCombobox<UserGroup>({
    forceVisible: true
  });

  async function removeFromGroup(group: UserGroup) {
    try {
      const success = await intric.userGroups.removeUser({ userGroup: group, user });
      if (success) {
        const index = selectedGroups.findIndex((current) => current.id === group.id);
        selectedGroups = selectedGroups.toSpliced(index, 1);
      }
    } catch (e) {
      alert(e);
      console.error(e);
    }
  }

  async function addToGroup() {
    if ($selected) {
      try {
        const group = $selected.value;
        // If the group is already added to the user, do not try to add it
        if (selectedGroups.find((curr) => curr.id === group.id)) {
          $selected = undefined;
          return;
        }

        const success = await intric.userGroups.addUser({ userGroup: group, user });
        if (success) {
          selectedGroups = [...selectedGroups, group];
          $selected = undefined;
        }
      } catch (e) {
        alert(e);
        console.error(e);
      }
    }
  }

  $: allGroups = (() => {
    const ids = selectedGroups.flatMap(({ id }) => id);
    return userGroups.filter(({ id }) => !ids.includes(id));
  })();

  $: filteredGroups = $touchedInput
    ? allGroups.filter(({ name }) => {
        const normalizedInput = $inputValue.toLowerCase();
        return name.toLowerCase().includes(normalizedInput);
      })
    : allGroups;

  $: if (!$open) {
    $inputValue = $selected?.label ?? "";
  }

  let inputElement: HTMLInputElement;
</script>

<div class="px-4 py-4">
  <div class="flex flex-col gap-1 pb-4">
    <div>
      <span class="pl-3 font-medium">User groups</span>
    </div>

    <div class="flex items-center justify-between gap-2">
      <div class="relative flex w-full">
        <input
          bind:this={inputElement}
          placeholder="Select a user group..."
          {...$input}
          use:input
          class="h-10 w-full items-center justify-between overflow-hidden rounded-lg
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
            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </button>
      </div>
      <Button variant="primary" disabled={$inputValue === ""} on:click={addToGroup}>Assign</Button>
    </div>
  </div>

  {#if selectedGroups.length > 0}
    <div class="overflow-clip rounded-md border border-stone-300 bg-stone-50">
      {#each selectedGroups as selectedGroup}
        <div
          class="flex w-full items-center justify-between border-b border-stone-200 py-2 pl-4 pr-2 last-of-type:border-b-0 hover:bg-white"
        >
          <div>
            {selectedGroup.name}
          </div>
          <Button
            destructive
            on:click={() => {
              removeFromGroup(selectedGroup);
            }}>Remove</Button
          >
        </div>
      {/each}
    </div>
  {/if}
</div>

{#if $open}
  <ul
    class="z-10 flex flex-col gap-1 overflow-y-auto rounded-lg border border-stone-300 bg-white p-1 shadow-md shadow-stone-200 focus:!ring-0"
    {...$menu}
    use:menu
  >
    <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
    <div class="flex max-h-full flex-col gap-0 overflow-y-auto bg-white text-black" tabindex="0">
      {#each filteredGroups as group, index (index)}
        <li
          {...$option({ value: group, label: group.name })}
          use:option
          class="flex items-center gap-1 rounded-md px-2 hover:cursor-pointer hover:bg-stone-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2.5"
            stroke="currentColor"
            class="h-5 w-5 {$isSelected(group) ? 'block' : 'hidden'} text-blue-600"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
          </svg>
          <div class="py-1">
            {group.name}
          </div>
        </li>
      {:else}
        <li
          class="flex items-center gap-1 rounded-md px-2 py-1 hover:cursor-pointer hover:bg-stone-200"
        >
          No results found
        </li>
      {/each}
    </div>
  </ul>
{/if}
