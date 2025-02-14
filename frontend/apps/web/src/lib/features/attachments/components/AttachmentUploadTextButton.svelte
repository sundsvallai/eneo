<script lang="ts">
  import { getAttachmentManager } from "../AttachmentManager";
  import { IconUpload } from "@intric/icons/upload";

  export let multiple: true | undefined = undefined;

  const {
    state: { attachmentRules },
    queueValidUploads
  } = getAttachmentManager();

  let fileInput: HTMLInputElement;

  function uploadFiles() {
    if (!fileInput.files) return;

    const errors = queueValidUploads([...fileInput.files]);

    if (errors) {
      alert(errors.join("\n"));
    }

    fileInput.value = "";
  }
</script>

<label
  for="fileInput"
  class="flex h-12 w-full cursor-pointer items-center justify-center gap-2 rounded-lg border border-default hover:bg-hover-stronger"
>
  <IconUpload />
  <span>Upload attachment</span>
  <input
    type="file"
    bind:this={fileInput}
    aria-label="Select a file to send to the service"
    id="fileInput"
    {multiple}
    accept={$attachmentRules.acceptString}
    on:change={uploadFiles}
    class="pointer-events-none absolute h-0 w-0 rounded-lg file:border-none file:bg-transparent file:text-transparent"
  />
</label>
