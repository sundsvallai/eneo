<script lang="ts">
  import { invalidate } from "$app/navigation";
  import SelectRole from "./SelectRole.svelte";
  import { Dialog, Button, Input } from "@intric/ui";
  import { getIntric } from "$lib/core/Intric";
  import { getAdminUserCtx } from "../ctx";
  import { getAppContext } from "$lib/core/AppContext";
  import InviteLinkDialog from "./InviteLinkDialog.svelte";

  const intric = getIntric();
  const { defaultRoles } = getAdminUserCtx();
  const { tenant } = getAppContext();

  let userRole = defaultRoles[0];
  let userEmail = "";
  let emailIsValid: boolean;
  let showDialog: Dialog.OpenState;
  let showInviteLink: Dialog.OpenState;

  async function inviteUser() {
    if (!userRole || !emailIsValid) return;

    try {
      await intric.users.invite({
        email: userEmail,
        predefined_role: userRole
      });
      invalidate("admin:users:load");
      $showDialog = false;
      $showInviteLink = true;
    } catch (e) {
      alert(e);
    }
  }
</script>

<InviteLinkDialog bind:isOpen={showInviteLink} user={{ email: userEmail }}></InviteLinkDialog>

<Dialog.Root bind:isOpen={showDialog}>
  <Dialog.Trigger asFragment let:trigger>
    <Button is={trigger} variant="primary">Create invitation</Button>
  </Dialog.Trigger>

  <Dialog.Content width="medium" form>
    <Dialog.Title>Invite a new user to {tenant.display_name}</Dialog.Title>

    <Dialog.Section>
      <Input.Text
        bind:isValid={emailIsValid}
        bind:value={userEmail}
        label="Email"
        required
        type="email"
        class="border-default hover:bg-hover-dimmer border-b px-4 py-4"
      ></Input.Text>

      <SelectRole availableRoles={defaultRoles} bind:value={userRole}></SelectRole>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="primary" on:click={inviteUser}>Create invitation</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
