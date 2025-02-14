<script lang="ts">
  import AttachmentUploadIconButton from "$lib/features/attachments/components/AttachmentUploadIconButton.svelte";
  import { IconEnter } from "@intric/icons/enter";
  import { IconStopCircle } from "@intric/icons/stop-circle";
  import { Button, Tooltip } from "@intric/ui";
  import { getChatManager } from "../../ChatManager";
  import { getAttachmentManager } from "$lib/features/attachments/AttachmentManager";

  const {
    state: { isAskingQuestion },
    askQuestion
  } = getChatManager();

  const {
    state: { attachments, isUploading },
    clearUploads
  } = getAttachmentManager();

  export let scrollToBottom: () => void;

  let question = "";
  let textarea: HTMLTextAreaElement;
  let abortController: AbortController | undefined;

  function ask() {
    if (isAskingDisabled) return;
    const files = $attachments.map((file) => file?.fileRef).filter((file) => file !== undefined);
    abortController = new AbortController();
    askQuestion(question, files, abortController, scrollToBottom);
    question = "";
    textarea.style.height = "auto";
    clearUploads();
  }

  $: isAskingDisabled =
    $isAskingQuestion || $isUploading || (question === "" && $attachments.length === 0);
</script>

<form
  class="flex w-[100%] max-w-[84ch] items-end justify-center gap-1 border-t border-default border-b-stronger bg-primary p-2 shadow-md md:w-full md:rounded-xl md:border md:p-1"
>
  <AttachmentUploadIconButton label="Upload documents to your conversation" />

  <textarea
    aria-label="Enter your question here"
    bind:this={textarea}
    bind:value={question}
    on:input={() => {
      textarea.style.height = "";
      const scrollHeight = Math.min(textarea.scrollHeight, 250);
      textarea.style.height = scrollHeight > 45 ? scrollHeight + "px" : "auto";
      textarea.style.overflowY = scrollHeight === 250 ? "auto" : "hidden";
    }}
    on:keypress={(e) => {
      if (e.which === 13 && !e.shiftKey) {
        e.preventDefault();
        ask();
      }
    }}
    name="question"
    id="question"
    placeholder="Ask a question..."
    rows="1"
    class="flex-grow resize-none overflow-y-auto rounded-lg bg-primary px-4 py-2 text-lg placeholder:text-secondary focus:outline-accent-default"
  ></textarea>

  {#if $isAskingQuestion}
    <Tooltip text={"Cancel your request"} placement="top" let:trigger asFragment>
      <Button
        unstyled
        aria-label="Cancel your request"
        type="submit"
        is={trigger}
        on:click={() => abortController?.abort("User cancelled")}
        name="ask"
        class="flex aspect-square h-11 min-h-11 w-11 min-w-11 items-center justify-center rounded-lg bg-secondary text-primary hover:bg-hover-stronger disabled:bg-tertiary disabled:text-secondary"
      >
        <IconStopCircle />
      </Button>
    </Tooltip>
  {:else}
    <Tooltip text={"Submit your question"} placement="top" let:trigger asFragment>
      <Button
        unstyled
        disabled={isAskingDisabled}
        aria-label="Submit your question"
        type="submit"
        is={trigger}
        on:click={() => ask()}
        name="ask"
        class=" flex h-11 w-11 items-center justify-center rounded-lg bg-secondary text-primary hover:bg-hover-stronger disabled:bg-tertiary disabled:text-secondary"
      >
        <IconEnter />
      </Button>
    </Tooltip>
  {/if}
</form>
