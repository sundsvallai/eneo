<script lang="ts">
  import type { Attachment } from "../AttachmentManager";
  import { IconCheck } from "@intric/icons/check";
  import { IconCancel } from "@intric/icons/cancel";
  import { IconFile } from "@intric/icons/file";
  import { Button, ProgressBar } from "@intric/ui";
  import { formatBytes } from "$lib/core/formatting/formatBytes";
  import { formatFileType } from "$lib/core/formatting/formatFileType";
  import { IconTrash } from "@intric/icons/trash";

  export let attachment: Attachment;
  export let borderOnLastItem = false;
</script>

<div
  class="flex h-16 items-center gap-4 border-b border-default px-4 hover:bg-hover-dimmer"
  class:last-of-type:border-b-0={!borderOnLastItem}
>
  <IconFile class="min-w-6"></IconFile>

  <div class="relative flex flex-grow flex-col gap-1 overflow-hidden">
    <div class="flex w-full items-center gap-4">
      <div class="flex flex-grow gap-2 overflow-hidden overflow-ellipsis break-words">
        <span class="line-clamp-1" class:font-medium={attachment.progress < 100}>
          {attachment.file.name}
        </span>
        {#if attachment.progress === 100}
          <IconCheck class="min-w-6 !stroke-2 text-positive-default" />
        {/if}
      </div>
      <span class="min-w-[8rem] text-right text-sm text-secondary">
        {formatFileType(attachment.file.type)} · {formatBytes(attachment.file.size)}
      </span>
    </div>

    {#if attachment.progress < 100}
      <ProgressBar progress={attachment.progress}></ProgressBar>
    {/if}
  </div>

  <div class="min-w-8">
    <Button
      variant="destructive"
      padding="icon"
      on:click={() => {
        attachment.remove();
      }}
    >
      {#if attachment.progress < 100}
        <IconCancel></IconCancel>
      {:else}
        <IconTrash></IconTrash>
      {/if}
    </Button>
  </div>
</div>
