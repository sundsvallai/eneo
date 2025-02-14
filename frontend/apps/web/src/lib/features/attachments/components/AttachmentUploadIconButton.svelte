<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconAttachment } from "@intric/icons/attachment";
  import { getAttachmentManager } from "$lib/features/attachments/AttachmentManager";
  import { Tooltip } from "@intric/ui";

  export let label = "Select documents to attach";
  let selectedFiles: FileList;

  const {
    state: { attachmentRules },
    queueValidUploads
  } = getAttachmentManager();

  function uploadFiles() {
    if (!selectedFiles) return;

    const errors = queueValidUploads([...selectedFiles]);

    if (errors) {
      alert(errors.join("\n"));
    }
  }
</script>

<Tooltip text={label}>
  <div class="flex h-11 w-11 items-center">
    <input
      type="file"
      accept={$attachmentRules.acceptString}
      bind:files={selectedFiles}
      aria-label={label}
      multiple
      id="fileInput"
      on:change={uploadFiles}
      class="pointer-events-none absolute h-11 w-11 rounded-lg file:border-none file:bg-transparent file:text-transparent"
    />
    <label
      for="fileInput"
      class="flex h-11 w-11 cursor-pointer items-center justify-center rounded-lg bg-secondary text-primary hover:bg-hover-stronger"
      ><IconAttachment class="!h-7 !w-7 text-primary" /></label
    >
  </div>
</Tooltip>
