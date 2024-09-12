<script lang="ts">
  import { invalidate } from "$app/navigation";
  import { getIntric } from "$lib/core/Intric";
  import type { InfoBlob } from "@intric/intric-js";
  import { Button, Dialog, Input } from "@intric/ui";

  const intric = getIntric();
  export let blob: InfoBlob;
  export let canEdit: boolean;

  let updatableTitle = blob.metadata.title ?? "";
  async function updateBlobName() {
    try {
      await intric.infoBlobs.update({
        blob: { id: blob.id },
        update: { metadata: { title: updatableTitle } }
      });
      invalidate("blobs:list");
      return true;
    } catch {
      return false;
    }
  }

  async function deleteBlob() {
    try {
      await intric.infoBlobs.delete(blob);
      invalidate("blobs:list");
      return true;
    } catch {
      return false;
    }
  }
</script>

{#if canEdit}
  <div class="flex items-center justify-end">
    <Dialog.Root>
      <Dialog.Trigger>Edit</Dialog.Trigger>

      <Dialog.Content>
        <Dialog.Title>Edit file</Dialog.Title>
        <Dialog.Description hidden>Enter new file name:</Dialog.Description>

        <Dialog.Section>
          <Input.Text
            bind:value={updatableTitle}
            class=" border-stone-100 px-4 py-4 hover:bg-stone-50">Name</Input.Text
          >
        </Dialog.Section>
        <Dialog.Controls let:close>
          <Button is={close}>Cancel</Button>
          <Button is={close} variant="outlined" on:click={updateBlobName}>Save changes</Button>
        </Dialog.Controls>
      </Dialog.Content>
    </Dialog.Root>

    <div class="w-2"></div>

    <Dialog.Root alert>
      <Dialog.Trigger asFragment let:trigger>
        <Button destructive is={trigger} label="Delete file" padding="icon">
          <svg
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
        <Dialog.Title>Delete group</Dialog.Title>
        <Dialog.Description
          >Do you really want to delete <span class="italic">{blob.metadata.title}</span
          >?</Dialog.Description
        >

        <Dialog.Controls let:close>
          <Button is={close}>Cancel</Button>
          <Button is={close} destructive on:click={deleteBlob}>Delete</Button>
        </Dialog.Controls>
      </Dialog.Content>
    </Dialog.Root>
  </div>
{/if}
