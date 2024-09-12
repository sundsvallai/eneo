<script lang="ts">
  import { invalidate } from "$app/navigation";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { type Group } from "@intric/intric-js";
  import { Button, Dialog, Input } from "@intric/ui";

  export let disabled = false;
  export let collection: Group;
  const intric = getIntric();
  const { refreshCurrentSpace } = getSpacesManager();

  let title: string = "";
  let text: string = "";
  let isUploading = false;

  async function uploadText() {
    if (title === "" || text === "") {
      return;
    }

    try {
      isUploading = true;
      await intric.infoBlobs.create({ group_id: collection.id, text, metadata: { title } });
      refreshCurrentSpace();
      invalidate("blobs:list");
      $showDialog = false;
      isUploading = false;
      text = title = "";
      return;
    } catch (e) {
      alert(e);
    }
  }

  let showDialog: Dialog.OpenState;
</script>

<Dialog.Root bind:isOpen={showDialog}>
  <Dialog.Trigger asFragment let:trigger>
    <Button {disabled} variant="primary" is={trigger}>Add text</Button>
  </Dialog.Trigger>

  <Dialog.Content wide form>
    <Dialog.Title>Add text</Dialog.Title>
    <Dialog.Description hidden></Dialog.Description>

    <Dialog.Section>
      <Input.Text
        bind:value={title}
        required
        class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50">Title</Input.Text
      >

      <Input.TextArea
        bind:value={text}
        required
        rows={15}
        class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50">Content</Input.TextArea
      >
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="primary" on:click={uploadText}>
        {#if isUploading}Submitting...{:else}
          Submit{/if}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
