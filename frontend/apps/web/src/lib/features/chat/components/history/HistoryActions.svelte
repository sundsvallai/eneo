<script lang="ts">
  import { IconTrash } from "@intric/icons/trash";
  import { Button, Dialog } from "@intric/ui";
  import { getChatService } from "../../ChatService.svelte";
  import type { ConversationSparse } from "@intric/intric-js";

  export let conversation: ConversationSparse;
  export let onConversationDeleted: ((conversation: ConversationSparse) => void) | undefined =
    undefined;

  const chat = getChatService();
</script>

<div class="flex items-center justify-end">
  <Dialog.Root alert>
    <Dialog.Trigger asFragment let:trigger>
      <Button variant="destructive" is={trigger} label="Delete conversation" padding="icon">
        <IconTrash />
      </Button>
    </Dialog.Trigger>

    <Dialog.Content width="small">
      <Dialog.Title>Delete conversation</Dialog.Title>
      <Dialog.Description
        >Do you really want to delete <span class="italic">{conversation.name.slice(0, 200)}</span
        >?</Dialog.Description
      >

      <Dialog.Controls let:close>
        <Button is={close}>Cancel</Button>
        <Button
          is={close}
          variant="destructive"
          on:click={async () => {
            await chat.deleteConversation(conversation);
            onConversationDeleted?.(conversation);
          }}>Delete</Button
        >
      </Dialog.Controls>
    </Dialog.Content>
  </Dialog.Root>
</div>
