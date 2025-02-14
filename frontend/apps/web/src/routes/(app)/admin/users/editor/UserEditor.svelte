<script lang="ts">
  import { invalidate } from "$app/navigation";
  import SelectRole from "./SelectRole.svelte";
  import { type User } from "@intric/intric-js";
  import { Dialog, Button, Input } from "@intric/ui";
  import { getIntric } from "$lib/core/Intric";
  import { getAdminUserCtx } from "../ctx";
  import { getAppContext } from "$lib/core/AppContext";

  const intric = getIntric();
  const { defaultRoles } = getAdminUserCtx();
  const { user: currentUser } = getAppContext();

  export let user: User;

  let userRole = user.predefined_roles.length > 0 ? user.predefined_roles[0] : defaultRoles[0];
  export let isOpen: Dialog.OpenState;

  async function updateUser() {
    if (!userRole) return;

    if (user.id === currentUser.id && !userRole.permissions.includes("admin")) {
      if (
        !confirm(
          `This will change your role to ${userRole.name} and remove your admin priviledges. You will no longer be able to access this page.\n\nAre you sure you want to continue?`
        )
      ) {
        return;
      }
    }

    try {
      await intric.users.update({
        user: { id: user.id },
        update: { predefined_role: userRole }
      });
      invalidate("admin:users:load");
      $isOpen = false;
    } catch (e) {
      alert(e);
    }
  }
</script>

<Dialog.Root bind:isOpen>
  <Dialog.Content width="medium" form>
    <Dialog.Title>Edit user</Dialog.Title>
    <Dialog.Description hidden>Edit the selected user</Dialog.Description>

    <Dialog.Section>
      <Input.Text
        bind:value={user.email}
        label="Email"
        disabled
        type="email"
        class="border-b border-default px-4 py-4 hover:bg-hover-dimmer"
      ></Input.Text>

      <SelectRole availableRoles={defaultRoles} bind:value={userRole}></SelectRole>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>

      <Button variant="primary" on:click={updateUser}>Save changes</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
