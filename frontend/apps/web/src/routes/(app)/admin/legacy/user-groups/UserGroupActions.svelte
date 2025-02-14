<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconTrash } from "@intric/icons/trash";
  import { Button, Dialog } from "@intric/ui";
  import type { UserGroup } from "@intric/intric-js";
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
    <Button is={trigger} label="Delete user group" variant="destructive" padding="icon">
      <IconTrash />
    </Button>
  </Dialog.Trigger>

  <Dialog.Content width="small">
    <Dialog.Title>Delete user group</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{userGroup.name}</span
      >?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button disabled={isDeleting} variant="destructive" on:click={deleteResource}
        >{isDeleting ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
