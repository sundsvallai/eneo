<script lang="ts">
  import { page } from "$app/stores";
  import { getAppContext } from "$lib/core/AppContext";
  import { Button, Dialog } from "@intric/ui";

  const { tenant } = getAppContext();

  export let user: { email: string };
  export let isOpen: Dialog.OpenState;

  $: inviteLink = `${$page.url.origin}/invite/${tenant.zitadel_org_id}`;

  function copyInviteLink() {
    try {
      navigator.clipboard.writeText(inviteLink);
      copyButtonText = "Copied!";
      setTimeout(() => {
        copyButtonText = "Copy invite link";
      }, 2000);
    } catch (error) {
      alert("Could not copy link.");
    }
  }

  let copyButtonText = "Copy invite link";
</script>

<Dialog.Root bind:isOpen>
  <Dialog.Content width="medium" form>
    <Dialog.Title>Your invite link</Dialog.Title>

    <Dialog.Section>
      <div class="flex flex-col gap-4 p-4">
        <p>
          Send <span class="italice">{user.email}</span> the link below so they can create their account.
        </p>
        <p
          class="border-accent-default bg-accent-dimmer text-accent-stronger border-l-2 px-4 py-2 text-sm"
        >
          <span class="font-bold">Note:</span> Please make sure they sign up with the same email address
          you have registered.
        </p>
        <div class="bg-primary flex items-center justify-between rounded-lg border p-1 shadow-sm">
          <span class="pl-2 font-mono">{inviteLink}</span>
          <Button variant="outlined" on:click={copyInviteLink}>{copyButtonText}</Button>
        </div>
      </div>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button variant="primary" is={close}>Done</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
