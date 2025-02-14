<script lang="ts">
  import { IconTrash } from "@intric/icons/trash";
  import { Button, Dialog } from "@intric/ui";
  import { getChatManager } from "../../ChatManager";
  import type { AssistantSession } from "@intric/intric-js";

  export let session: { id: string; name: string };
  export let onSessionDeleted: ((session: AssistantSession) => void) | undefined = undefined;

  const { deleteSession } = getChatManager();
</script>

<div class="flex items-center justify-end">
  <Dialog.Root alert>
    <Dialog.Trigger asFragment let:trigger>
      <Button variant="destructive" is={trigger} label="Delete session" padding="icon">
        <IconTrash />
      </Button>
    </Dialog.Trigger>

    <Dialog.Content width="small">
      <Dialog.Title>Delete session</Dialog.Title>
      <Dialog.Description
        >Do you really want to delete <span class="italic">{session.name}</span
        >?</Dialog.Description
      >

      <Dialog.Controls let:close>
        <Button is={close}>Cancel</Button>
        <Button
          is={close}
          variant="destructive"
          on:click={async () => {
            await deleteSession(session);
            onSessionDeleted?.(session);
          }}>Delete</Button
        >
      </Dialog.Controls>
    </Dialog.Content>
  </Dialog.Root>
</div>
