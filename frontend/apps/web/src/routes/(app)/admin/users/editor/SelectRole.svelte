<script lang="ts">
  import type { Role } from "@intric/intric-js";
  import { Select } from "@intric/ui";
  import { writable } from "svelte/store";

  // Array of all currently selected roles
  export let value: Role;

  // Array of all available roles
  export let availableRoles: Role[];

  const roleSelectStore = writable({
    label: availableRoles.find((role) => role.id === value.id)?.name ?? "Role not available",
    value
  });

  $: value = $roleSelectStore.value;
</script>

<Select.Root
  customStore={roleSelectStore}
  class="border-b border-default px-4 py-4 hover:bg-hover-dimmer"
>
  <Select.Label>Roles & Permissions</Select.Label>
  <Select.Trigger placeholder="Select..."></Select.Trigger>
  <Select.Options>
    {#each availableRoles as role}
      <Select.Item value={role} label={role.name}>
        <div class="flex w-full items-center justify-between py-1">
          <span>
            {role.name}
          </span>
        </div>
      </Select.Item>
    {/each}
  </Select.Options>
</Select.Root>
