<!-- MIT License -->

<script lang="ts">
  import type { Role } from "@intric/intric-js";
  import { Select } from "@intric/ui";
  import { writable } from "svelte/store";

  // Array of all currently selected roles
  export let value: Role[];

  // Array of all available roles
  export let defaultRoles: Role[];
  export let customRoles: Role[];

  const allRoles = [...customRoles, ...defaultRoles];

  function getStoreValue() {
    const selectedIds = value.map((role) => role.id);
    const selectedRoles = allRoles.filter((role) => selectedIds.includes(role.id));
    return selectedRoles.map((role) => {
      return {
        value: role,
        label: role.name
      };
    });
  }

  function setValue() {
    value = $roleSelectStore.map((item) => item.value);
  }

  let roleSelectStore = writable(getStoreValue());
  $: setValue(), $roleSelectStore;
</script>

{#if allRoles.length > 0}
  <Select.Root
    multiple
    customStore={roleSelectStore}
    class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50"
  >
    <Select.Label>Roles & Permissions</Select.Label>
    <Select.Trigger placeholder="Select..."></Select.Trigger>
    <Select.Options>
      <Select.OptionGroup label="Default Roles">
        {#each defaultRoles as role}
          <Select.Item value={role} label={role.name}>
            <div class="flex w-full items-center justify-between py-1">
              <span>
                {role.name}
              </span>
            </div>
          </Select.Item>
        {/each}
      </Select.OptionGroup>
      {#if customRoles.length > 0}
        <Select.OptionGroup label="Custom roles">
          {#each customRoles as role}
            <Select.Item value={role} label={role.name}></Select.Item>
          {/each}
        </Select.OptionGroup>
      {/if}
    </Select.Options>
  </Select.Root>
{/if}
