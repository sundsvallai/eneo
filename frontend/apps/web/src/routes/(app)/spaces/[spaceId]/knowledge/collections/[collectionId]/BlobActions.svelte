<script lang="ts">
  import { IconTrash } from "@intric/icons/trash";
  import { Button, Dialog, Dropdown, Input } from "@intric/ui";
  import { invalidate } from "$app/navigation";
  import { getIntric } from "$lib/core/Intric";
  import type { InfoBlob } from "@intric/intric-js";
  import { IconEllipsis } from "@intric/icons/ellipsis";
  import { IconEdit } from "@intric/icons/edit";

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
    } catch (e) {
      alert(`Could not change title  to ${updatableTitle}`);
      console.error(e);
      return false;
    }
  }

  async function deleteBlob() {
    try {
      await intric.infoBlobs.delete(blob);
      invalidate("blobs:list");
      return true;
    } catch (e) {
      alert(`Could not delete ${blob.metadata.title ?? "this file"}`);
      console.error(e);
      return false;
    }
  }

  let showDeleteDialog: Dialog.OpenState;
  let showEditDialog: Dialog.OpenState;
</script>

{#if canEdit}
  <Dropdown.Root>
    <Dropdown.Trigger asFragment let:trigger>
      <Button is={trigger} padding="icon">
        <IconEllipsis />
      </Button>
    </Dropdown.Trigger>

    <Dropdown.Menu let:item>
      <Button
        is={item}
        on:click={() => {
          $showEditDialog = true;
        }}
        padding="icon-leading"
      >
        <IconEdit size="sm" />
        Edit</Button
      >
      <Button
        is={item}
        variant="destructive"
        on:click={() => {
          $showDeleteDialog = true;
        }}
        padding="icon-leading"
      >
        <IconTrash size="sm" />Delete</Button
      >
    </Dropdown.Menu>
  </Dropdown.Root>
{/if}

<Dialog.Root bind:isOpen={showEditDialog}>
  <Dialog.Content width="small">
    <Dialog.Title>Edit file</Dialog.Title>
    <Dialog.Description hidden>Enter new file name:</Dialog.Description>

    <Dialog.Section>
      <Input.Text
        bind:value={updatableTitle}
        label="Name"
        class=" border-default hover:bg-hover-dimmer px-4 py-4"
      ></Input.Text>
    </Dialog.Section>
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button is={close} variant="primary" on:click={updateBlobName}>Save changes</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<Dialog.Root alert bind:isOpen={showDeleteDialog}>
  <Dialog.Content width="small">
    <Dialog.Title>Delete group</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{blob.metadata.title}</span
      >?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button is={close} variant="destructive" on:click={deleteBlob}>Delete</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
