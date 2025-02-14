<script lang="ts">
  import { getIntric } from "$lib/core/Intric";
  import { initAttachmentManager } from "$lib/features/attachments/AttachmentManager";
  import AttachmentDropArea from "$lib/features/attachments/components/AttachmentDropArea.svelte";
  import { getAttachmentRulesStore } from "$lib/features/attachments/getAttachmentRules";
  import { getChatManager } from "../../ChatManager";
  import Message from "./Message.svelte";
  import SessionAttachments from "./SessionAttachments.svelte";
  import SessionInput from "./SessionInput.svelte";

  const {
    state: { currentSession, assistant, isAskingQuestion }
  } = getChatManager();

  const attachmentRules = getAttachmentRulesStore(assistant);
  initAttachmentManager({ intric: getIntric(), options: { rules: attachmentRules } });

  let scrollContainer: HTMLDivElement;
  let userScrolledUp = false;
  const scrollToBottom = () => {
    if (!userScrolledUp && scrollContainer) {
      setTimeout(() => {
        scrollContainer.scrollTo({ top: scrollContainer.scrollHeight });
      }, 10);
    }
  };

  const handleScroll = () => {
    const bottomThreshold = 250; // px from bottom to still consider it "at bottom"
    const distanceFromBottom =
      scrollContainer.scrollHeight - scrollContainer.clientHeight - scrollContainer.scrollTop;
    userScrolledUp = distanceFromBottom > bottomThreshold;
  };

  let isDragging = false;
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  class="md:stable-gutter relative flex h-full flex-col overflow-y-auto"
  bind:this={scrollContainer}
  on:scroll={handleScroll}
  on:dragenter={(event) => {
    event.preventDefault();
    isDragging = true;
  }}
>
  {#if $currentSession.messages && $currentSession.messages.length > 0}
    <div class="flex flex-grow flex-col gap-2 p-4 md:p-8" aria-live="polite">
      {#each $currentSession.messages as message, idx}
        <Message
          {message}
          isLast={idx === $currentSession.messages.length - 1}
          isLoading={$isAskingQuestion}
        ></Message>
      {/each}
    </div>
  {:else if $$slots.default}
    <div class="flex flex-grow flex-col items-center justify-center">
      <slot></slot>
    </div>
  {:else}
    <div class="flex flex-grow items-center justify-center">
      <p class="text-center text-primary">
        Hi, I'm <span class="tex-primary italic">{$assistant.name}!</span><br />Ask me anything to
        get started.
      </p>
    </div>
  {/if}
  <div
    class="sticky inset-x-0 bottom-0 flex flex-col items-center justify-end gap-2 bg-gradient-to-b from-transparent to-[var(--background-primary)] p-0 backdrop-blur-sm md:gap-4 md:p-6 md:pt-0"
  >
    <SessionAttachments></SessionAttachments>
    <SessionInput {scrollToBottom}></SessionInput>
  </div>
</div>
{#if isDragging}
  <AttachmentDropArea bind:isDragging label="Drop files here to attach them to your conversation" />
{/if}
