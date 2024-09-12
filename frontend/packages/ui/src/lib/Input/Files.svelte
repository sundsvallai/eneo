<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import type { FileSystemEntry, FileSystemDirectoryEntry, FileSystemFileEntry } from "./types.js";

  /** Name of the file input field, defaults to `dropzoneInput` */
  export let name = "dropzoneInput";
  export let acceptedMimeTypes = ["text/plain"];
  export let files: File[] = [];

  let dropzone: HTMLDivElement;
  let dropzoneInput: HTMLInputElement;

  let isDragging = false;

  const dispatch = createEventDispatcher();

  function addFocusDecoration() {
    dropzone.classList.add("focused");
  }

  function removeFocusDecoration() {
    dropzone.classList.remove("focused");
  }

  function handleDragOver(event: DragEvent) {
    addFocusDecoration();
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = "copy";
    }
  }

  function handleDragLeave(event: DragEvent) {
    const target = (event.relatedTarget as HTMLElement) ?? null;

    // If drag has ended or left dropzone remove focus deco
    // This event also fires when dragging over other elements inside the dropzone
    if (event.type === "dragend" || !target.classList.contains("dropzone")) {
      removeFocusDecoration();
    }
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    if (event.dataTransfer) {
      removeFocusDecoration();
      const items = event.dataTransfer.items;
      for (let i = 0; i < items.length; i++) {
        let entry = items[i].webkitGetAsEntry();
        scanEntry(entry);
      }
    }
  }

  function scanEntry(entry: FileSystemEntry | null) {
    if (entry) {
      if (entry.isFile) {
        (entry as FileSystemFileEntry).file((file) => addFiles([file]));
      } else if (entry.isDirectory) {
        const reader = (entry as FileSystemDirectoryEntry).createReader();
        reader.readEntries((entries) => {
          entries.forEach((entry) => scanEntry(entry));
        });
      }
    }
  }

  function handleClick() {
    dropzoneInput.click();
  }

  function handleInputChange() {
    addFiles([...(dropzoneInput.files ?? [])]);
  }

  function addFiles(newFiles: File[]) {
    const acceptedFiles: File[] = [];
    const rejectedFiles: File[] = [];

    // Simple check for format: we match file extension
    const fileTypeIsValid = (file: File) => acceptedMimeTypes.includes(file.type);

    // Simple check for duplicates: compare file name, size, and last edited
    const fileIsNotDuplicate = (file: File) =>
      files.find(
        (f) => f.name === file.name && f.size === file.size && f.lastModified === file.lastModified
      ) === undefined;

    for (const file of newFiles) {
      if (fileTypeIsValid(file) && fileIsNotDuplicate(file)) {
        acceptedFiles.push(file);
      } else {
        rejectedFiles.push(file);
      }
    }

    files = [...files, ...acceptedFiles];
    dispatch("fileselectionchanged", { files, rejectedFiles });
  }

  function removeFile(file: File) {
    files = files.filter((f) => f !== file);
    dispatch("fileselectionchanged", { files });
  }

  function handleGlobalDrag(e: DragEvent, state: { isDragging: boolean }) {
    e.preventDefault();
    isDragging = state.isDragging;
  }
</script>

<svelte:window
  on:drop={(e) => {
    handleGlobalDrag(e, { isDragging: false });
  }}
  on:dragover={(e) => {
    handleGlobalDrag(e, { isDragging: true });
  }}
  on:dragend={(e) => {
    handleGlobalDrag(e, { isDragging: false });
  }}
  on:dragleave={(e) => {
    // Only handle leave if leaving window
    if (e.relatedTarget == null) {
      handleGlobalDrag(e, { isDragging: false });
    }
  }}
/>

<div
  class="relative flex h-full max-h-[80vh] min-h-[50vh] w-full min-w-[200px] flex-col gap-2 overflow-y-auto rounded-lg border border-stone-300 bg-white p-2"
  bind:this={dropzone}
  on:dragenter={handleDragOver}
  on:dragover={handleDragOver}
  on:dragleave={handleDragLeave}
  on:dragend={handleDragLeave}
  on:drop={handleDrop}
  role="button"
  tabindex="0"
>
  {#if files.length > 0}
    {#each files as file (file.name + file.lastModified + file.size)}
      <div
        class="flex cursor-default items-center justify-between rounded-md border border-stone-200 p-2 hover:bg-stone-50"
      >
        <div class="flex items-center gap-2">
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
              d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12-3-3m0 0-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
            />
          </svg>
          {file.name}
        </div>
        <button
          on:click={() => removeFile(file)}
          class="cursor-pointer rounded-full p-2 text-red-500 hover:bg-red-500 hover:text-white"
        >
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
        </button>
      </div>
    {/each}
  {:else}
    <button
      class="absolute inset-0 flex flex-col items-center justify-center rounded-lg text-stone-700 hover:bg-stone-100"
      on:click={handleClick}
      tabindex="0"
    >
      {#if !isDragging}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="0.7"
          stroke="currentColor"
          class="h-24 w-24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.233-2.33 3 3 0 0 1 3.758 3.848A3.752 3.752 0 0 1 18 19.5H6.75Z"
          />
        </svg>

        <div class="text-center">
          Drag and Drop files or folders here <br />
          or <span class="underline">Click to browse</span>.
        </div>
      {:else}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="0.7"
          stroke="currentColor"
          class="h-24 w-24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9 9V4.5M9 9H4.5M9 9 3.75 3.75M9 15v4.5M9 15H4.5M9 15l-5.25 5.25M15 9h4.5M15 9V4.5M15 9l5.25-5.25M15 15h4.5M15 15v4.5m0-4.5 5.25 5.25"
          />
        </svg>

        <div class="text-center">Drop your files here</div>
      {/if}
      <button
        class="pt-2 text-sm text-stone-400"
        on:click={() => {
          alert(
            "Currently we support the following MIME types for uploading:\n" +
              acceptedMimeTypes.join("\n")
          );
        }}
      >
        Click <span class="underline">here</span> to see a list of supported filetypes.
      </button>
    </button>
  {/if}
  <input
    bind:this={dropzoneInput}
    type="file"
    multiple
    {name}
    accept={acceptedMimeTypes.join(",")}
    on:change={handleInputChange}
    on:focus={addFocusDecoration}
    on:blur={removeFocusDecoration}
    class="hidden h-0 w-0"
  />
</div>
