<!-- MIT License -->
<script lang="ts">
  import IconUpload from "$lib/components/icons/IconUpload.svelte";
  import { getFileUploadManager } from "../FileUploadManager";

  export let isDragging: boolean;
  export let imagesAllowed: boolean = false;

  const { queueUploads } = getFileUploadManager();

  let handleDragLeave = (event: DragEvent) => {
    event.preventDefault();
    isDragging = false;
  };

  let handleDragOver = (event: DragEvent) => {
    event.preventDefault();
    isDragging = true;
  };

  const handleDrop = (event: DragEvent) => {
    event.preventDefault();
    isDragging = false;
    if (event.dataTransfer && event.dataTransfer.files) {
      let filesToUpload = event.dataTransfer.files;
      queueUploads(Array.from(filesToUpload));
    }
  };
</script>

<form
  on:dragover={handleDragOver}
  on:drop={handleDrop}
  on:dragleave={handleDragLeave}
  class="absolute inset-0 z-10 flex items-center justify-center p-8 pl-0"
>
  <div
    class="pointer-events-none flex h-full w-full items-center justify-center gap-2 rounded-md border border-black/25 bg-gradient-to-tr from-stone-50 to-stone-100 p-4 shadow-xl"
  >
    <div
      class=" flex h-full w-full flex-col items-center justify-center gap-4 rounded border-2 border-dashed border-stone-300"
    >
      <IconUpload size="large" class="!h-14 !w-14 stroke-stone-300" />
      <p class="text-center text-stone-500">
        Drop {imagesAllowed ? "documents or images" : "documents"} here to add them to your conversation
      </p>
    </div>
  </div>
</form>
