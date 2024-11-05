<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import type { UserGroup } from "@intric/intric-js";
  import { Button, Dialog } from "@intric/ui";
  import UserGroupEditor from "./UserGroupEditor.svelte";
  import { getIntric } from "$lib/core/Intric";
  import { invalidate } from "$app/navigation";

  export let userGroup: UserGroup;

  const intric = getIntric();

  let isDeleting = false;
  let showDeleteDialog: Dialog.OpenState;
  async function deleteResource() {
    isDeleting = true;
    try {
      await intric.userGroups.delete(userGroup);
      invalidate("admin:user-groups:load");
      $showDeleteDialog = false;
    } catch (e) {
      alert("Could not delete user group.");
      console.error(e);
    }
    isDeleting = false;
  }
</script>

<UserGroupEditor {userGroup} mode="update"></UserGroupEditor>

<div class="w-2"></div>

<Dialog.Root alert bind:isOpen={showDeleteDialog}>
  <Dialog.Trigger asFragment let:trigger>
    <Button is={trigger} label="Delete user group" destructive padding="icon"
      ><svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="h-6 w-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
        />
      </svg>
    </Button>
  </Dialog.Trigger>

  <Dialog.Content>
    <Dialog.Title>Delete user group</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{userGroup.name}</span
      >?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button disabled={isDeleting} destructive on:click={deleteResource}
        >{isDeleting ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
