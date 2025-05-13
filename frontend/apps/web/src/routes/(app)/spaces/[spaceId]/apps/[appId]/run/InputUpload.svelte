<script lang="ts">
  import { IconUpload } from "@intric/icons/upload";
  import type { App } from "@intric/intric-js";
  import { getAttachmentManager } from "$lib/features/attachments/AttachmentManager";
  import { getExplicitAttachmentRules } from "$lib/features/attachments/getAttachmentRules";
  import AttachmentItem from "$lib/features/attachments/components/AttachmentItem.svelte";

  export let input: App["input_fields"][number];
  export let description: string = "Upload files to send to this app.";

  const attachmentRules = getExplicitAttachmentRules(input);
  let fileInput: HTMLInputElement;

  const {
    queueValidUploads,
    state: { attachments }
  } = getAttachmentManager();

  function uploadFiles() {
    if (!fileInput.files) return;

    const errors = queueValidUploads([...fileInput.files], attachmentRules);

    if (errors) {
      alert(errors.join("\n"));
    }

    fileInput.value = "";
  }
</script>

{#if $attachments.length > 0}
  <div class="border-default bg-primary w-[60ch] rounded-lg border p-2">
    <div class="flex flex-col">
      {#each $attachments as attachment (attachment.id)}
        <AttachmentItem {attachment}></AttachmentItem>
      {/each}
    </div>
  </div>
{/if}

{#if attachmentRules.maxTotalCount ? $attachments.length < attachmentRules.maxTotalCount : true}
  <label
    for="fileInput"
    class="border-stronger bg-primary hover:border-stronger hover:bg-dynamic-default hover:text-on-fill flex cursor-pointer gap-2 rounded-full border px-6 py-3 text-lg shadow-lg"
  >
    <IconUpload></IconUpload>
    {description}</label
  >
  <input
    type="file"
    bind:this={fileInput}
    id="fileInput"
    accept={attachmentRules.acceptString}
    multiple={true}
    on:change={uploadFiles}
    class="pointer-events-none absolute h-11 w-11 rounded-lg file:border-none file:bg-transparent file:text-transparent"
  />
{/if}
