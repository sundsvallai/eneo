<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { getJobManager } from "$lib/features/jobs/JobManager";
  import { type Group, type InfoBlob } from "@intric/intric-js";
  import { Button, Dialog, Input } from "@intric/ui";

  const {
    limits,
    state: { showHeader }
  } = getAppContext();
  const acceptedMimeTypes = limits.info_blobs.formats.map((format) => format.mimetype);

  const {
    queueUploads,
    state: { showJobManagerPanel }
  } = getJobManager();
  export let collection: Group;
  export let currentBlobs: InfoBlob[];
  export let disabled = false;

  let files: File[] = [];
  let isUploading = false;

  async function uploadBlobs() {
    const duplicateFiles: string[] = [];
    const blobTitles = currentBlobs.flatMap((blob) => blob.metadata.title);
    files.forEach((file) => {
      if (blobTitles.includes(file.name)) {
        duplicateFiles.push(file.name);
      }
    });

    if (duplicateFiles.length > 0) {
      if (
        !confirm(
          `The following files already exist on the server:\n- ${duplicateFiles.join("\n- ")}\nProceeding will replace them with the newly uploaded file(s).`
        )
      ) {
        return;
      }
    }

    try {
      isUploading = true;
      queueUploads(collection.id, files);
      $showHeader = true;
      $showJobManagerPanel = true;
      $showDialog = false;
      isUploading = false;
      files = [];
      return;
    } catch (e) {
      alert(e);
    }
  }

  let showDialog: Dialog.OpenState;
</script>

<Dialog.Root
  bind:isOpen={showDialog}
  on:close={() => {
    files = [];
  }}
>
  <Dialog.Trigger asFragment let:trigger>
    <Button {disabled} variant="primary" is={trigger}>Upload files</Button>
  </Dialog.Trigger>

  <Dialog.Content width="medium">
    <Dialog.Title>Upload files</Dialog.Title>
    <Dialog.Description hidden></Dialog.Description>

    <Input.Files bind:files {acceptedMimeTypes}></Input.Files>

    <Dialog.Controls let:close>
      {#if files.length > 0}
        <Button
          on:click={() => {
            files = [];
          }}
          variant="destructive">Clear list</Button
        >
        <div class="flex-grow"></div>
      {/if}
      <Button is={close}>Cancel</Button>
      <Button variant="primary" on:click={uploadBlobs} disabled={isUploading || files.length < 1}>
        {#if isUploading}Uploading...{:else}
          Upload files{/if}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
