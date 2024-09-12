<script lang="ts">
  import IconDocument from "$lib/components/icons/IconDocument.svelte";
  import ChatFileUpload from "$lib/features/file-uploads/components/ChatFileUpload.svelte";
  import { getFileUploadManager } from "$lib/features/file-uploads/FileUploadManager";
  import LoadingSpinner from "$lib/components/icons/LoadingSpinner.svelte";
  import IconTrash from "$lib/components/icons/IconTrash.svelte";
  import type { Assistant, UploadedFile } from "@intric/intric-js";
  import { Tooltip } from "@intric/ui";
  import { page } from "$app/stores";

  export let askQuestion: (question: string, files: UploadedFile[]) => Promise<void>;
  export let assistant: Assistant;

  const {
    state: { uploads, isBusy },
    removeUpload,
    clearUploads
  } = getFileUploadManager();

  let textarea: HTMLTextAreaElement;
  let question = "";
  let loadingAnswer: boolean;

  // If the page url changes, we know that we are no longer in the original session.
  // This can happen when quick switching assistants.
  // In that case we want the user to be able to ask a new question.
  $: if ($page.url.pathname) {
    loadingAnswer = false;
  }

  async function ask() {
    if (loadingAnswer || $isBusy) return;
    if (question === "" && $uploads.length === 0) return;
    loadingAnswer = true;
    const files = $uploads.map((file) => file?.fileRef).filter((f) => f !== undefined);
    try {
      askQuestion(question, files).then(() => (loadingAnswer = false));
    } catch (e) {
      alert(e);
      loadingAnswer = false;
    }
    clearUploads();
    question = "";
    textarea.style.height = "auto";
  }
</script>

<!-- File list  -->
<div class="flex w-full max-w-[72ch] flex-grow gap-3">
  {#if $uploads}
    {#each $uploads as upload}
      <div
        class="group relative flex items-center gap-3.5 rounded-md border border-stone-200 bg-white py-1.5 pl-1.5 pr-6 shadow-md hover:bg-stone-50"
      >
        <button
          on:click={() => upload.fileRef && removeUpload(upload.fileRef)}
          class="absolute -right-2 -top-2.5 flex h-6 w-6 items-center justify-center rounded-full border border-stone-200 bg-white p-0.5 text-black opacity-0 hover:bg-black hover:text-white group-hover:opacity-100"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2"
            stroke="currentColor"
            class="h-5 w-5"
          >
            Test
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
        <div
          class="flex h-12 w-12 items-center justify-center rounded-md {upload.status ===
          'uploading'
            ? 'bg-stone-200'
            : 'bg-blue-500'}"
        >
          <div class="relative flex h-full w-full items-center justify-center">
            {#if upload.status === "uploading"}
              <LoadingSpinner />
            {:else}
              <IconDocument class="stroke-white" />
            {/if}
            <button
              on:click={() => upload.fileRef && removeUpload(upload.fileRef)}
              class="absolute flex h-full w-full items-center justify-center rounded-md bg-red-500 opacity-0 hover:opacity-100"
            >
              <IconTrash class="stroke-white" />
            </button>
          </div>
        </div>
        <div>
          <div>
            {upload.file.name}
          </div>
          <div class="text-sm text-gray-500">
            {upload.file.type.split("/")[upload.file.type.split("/").length - 1].toUpperCase()}
          </div>
        </div>
      </div>
    {/each}
  {/if}
</div>
<!-- Chat input  -->
<form
  class="flex w-full max-w-[72ch] flex-grow items-end justify-center gap-0.5 overflow-clip rounded-lg border border-stone-300 bg-stone-100 p-0.5 shadow-md"
>
  <ChatFileUpload imagesAllowed={assistant.completion_model?.vision} />

  <textarea
    aria-label="Enter your question here"
    bind:this={textarea}
    bind:value={question}
    on:input={() => {
      textarea.style.height = "";
      const scrollHeight = Math.min(textarea.scrollHeight, 200);
      textarea.style.height = scrollHeight > 45 ? scrollHeight + "px" : "auto";
      textarea.style.overflowY = scrollHeight === 200 ? "auto" : "hidden";
    }}
    on:keypress={(e) => {
      if (e.which === 13 && !e.shiftKey) {
        e.preventDefault();
        ask();
      }
    }}
    name="question"
    id="question"
    rows="1"
    class="relative min-h-10 flex-grow resize-none overflow-y-auto rounded-md border border-stone-300 px-4 py-2 text-lg ring-stone-300 hover:border-stone-400 hover:ring-2"
  ></textarea>
  <Tooltip text={"Submit your question"}>
    <button
      aria-label="Submit your question"
      disabled={loadingAnswer || $isBusy || (question === "" && $uploads.length === 0)}
      type="submit"
      on:click={() => ask()}
      name="ask"
      class="rounded-lg border border-stone-100 bg-stone-100 p-2 text-lg hover:bg-stone-300 disabled:text-stone-300 disabled:hover:bg-stone-100"
    >
      {#if loadingAnswer}
        <LoadingSpinner />
      {:else}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-7 w-7"
          ><polyline points="9 10 4 15 9 20" /><path d="M20 4v7a4 4 0 0 1-4 4H4" /></svg
        >
      {/if}
    </button>
  </Tooltip>
</form>
