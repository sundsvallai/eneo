<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconTrash } from "@intric/icons/trash";
  import { Button, Dialog } from "@intric/ui";
  import { invalidate } from "$app/navigation";
  import type { User } from "@intric/intric-js";
  import UserEditor from "./editor/UserEditor.svelte";
  import { getAppContext } from "$lib/core/AppContext";
  import { getIntric } from "$lib/core/Intric";

  const intric = getIntric();
  export let user: User;

  async function deleteUser() {
    try {
      await intric.users.delete(user);
      invalidate("admin:users:load");
    } catch (e) {
      console.error(e);
    }
  }

  const { user: currentUser } = getAppContext();
</script>

<UserEditor {user} mode="update"></UserEditor>

<div class="w-2"></div>

<Dialog.Root alert>
  <Dialog.Trigger asFragment let:trigger>
    <Button
      is={trigger}
      label="Delete user"
      variant="destructive"
      padding="icon"
      disabled={user.username === currentUser.username}
    >
      <IconTrash />
    </Button>
  </Dialog.Trigger>

  <Dialog.Content width="small">
    <Dialog.Title>Delete user</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{user.username}</span>?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button is={close} variant="destructive" on:click={deleteUser}>Delete</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
