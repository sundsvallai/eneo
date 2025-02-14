<script lang="ts">
  import { IconTrash } from "@intric/icons/trash";
  import { IconDownload } from "@intric/icons/download";
  import { Button } from "@intric/ui";
  import { getAttachmentManager } from "$lib/features/attachments/AttachmentManager";
  import dayjs from "dayjs";
  import AudioRecorder from "./AudioRecorder.svelte";
  import AttachmentItem from "$lib/features/attachments/components/AttachmentItem.svelte";

  export let description = "Record audio on this device";

  const {
    queueValidUploads,
    state: { attachments }
  } = getAttachmentManager();

  let audioURL: string | undefined;
  let audioFile: File | undefined;

  async function saveAudioFile() {
    if (!audioFile) {
      alert("Recording not found");
      return;
    }
    const suggestedName = audioFile.name + (audioFile.type.includes("webm") ? ".webm" : ".mp4");
    if (window.showSaveFilePicker) {
      const handle = await window.showSaveFilePicker({ suggestedName });
      const writable = await handle.createWritable();
      await writable.write(audioFile);
      writable.close();
    } else {
      const a = document.createElement("a");
      a.download = suggestedName;
      a.href = URL.createObjectURL(audioFile);
      a.click();
      setTimeout(function () {
        URL.revokeObjectURL(a.href);
      }, 1500);
    }
  }
</script>

<span class="text-secondary">{description}</span>

{#if audioFile && audioURL}
  {#if $attachments.length > 0}
    {#each $attachments as attachment}
      <div class="w-[60ch] rounded-lg border border-stronger bg-primary p-2">
        <div class="flex flex-col">
          <AttachmentItem {attachment}></AttachmentItem>
        </div>
      </div>
    {/each}
  {:else}
    <audio controls src={audioURL} class="ml-2 h-12 rounded-full border border-stronger shadow-sm"
    ></audio>

    <div class="flex items-center gap-4">
      <Button
        variant="destructive"
        padding="icon-leading"
        on:click={() => {
          if (confirm("Do you really want to discard this recording?")) {
            audioFile = undefined;
            audioURL = undefined;
          }
        }}
      >
        <IconTrash />
        Discard</Button
      >
      <Button variant="outlined" on:click={saveAudioFile}><IconDownload />Save as file</Button>
      <Button
        variant="primary"
        on:click={() => {
          if (!audioFile) {
            alert("Recording not found");
            return;
          }
          const errors = queueValidUploads([audioFile]);
          if (errors) {
            alert(errors);
          }
        }}>Use this recording</Button
      >
    </div>
  {/if}
{:else}
  <AudioRecorder
    onRecordingDone={({ blob, mimeType }) => {
      const fileName = `Recording ${dayjs().format("YYYY-MM-DD HH:mm:ss")}`;
      audioFile = new File([blob], fileName, { type: mimeType });
      audioURL = URL.createObjectURL(blob);
    }}
  ></AudioRecorder>
{/if}
