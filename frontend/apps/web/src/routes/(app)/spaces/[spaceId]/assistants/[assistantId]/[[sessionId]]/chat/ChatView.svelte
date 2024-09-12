<script lang="ts">
  import type {
    Assistant,
    AssistantResponse,
    AssistantSession,
    UploadedFile
  } from "@intric/intric-js";
  import {
    createFileUploadManager,
    setFileUploadManager
  } from "$lib/features/file-uploads/FileUploadManager";
  import IconSession from "$lib/components/icons/IconSession.svelte";
  import ChatInput from "./ChatInput.svelte";
  import ChatMessage from "./ChatMessage.svelte";
  import { tick } from "svelte";
  import ChatDragAndDrop from "$lib/features/file-uploads/components/ChatDragAndDrop.svelte";
  import { getIntric } from "$lib/core/Intric";

  export let assistant: Assistant;
  export let session: Omit<AssistantSession, "id" | "messages"> & {
    id: string | null;
    messages: AssistantResponse[];
  };
  export let onSessionCreated: (newSession: typeof session) => Promise<void>;

  const intric = getIntric();
  setFileUploadManager(createFileUploadManager(intric));

  async function askQuestion(question: string, files: UploadedFile[]) {
    const initialSession = session;
    session.messages = [
      ...(session.messages ?? []),
      {
        question,
        answer: "",
        references: [],
        id: "",
        files
      }
    ];
    await tick();
    scrollToBottom();

    try {
      const completedMessage = await intric.assistants.ask({
        assistant,
        session,
        question,
        files: files.map((fileRef) => ({ id: fileRef.id })),
        onAnswer: (token) => {
          // If the session has changed, e.g. when switching to a different assistant,
          // we should no longer append messages to the current session.
          // TODO: Ideally this should cancel the whole "ask" request
          if (initialSession !== session) {
            return;
          }
          session.messages[session.messages.length - 1].answer += token;
          scrollToBottom();
        }
      });

      session.messages[session.messages.length - 1] = completedMessage;

      if (session.id === null) {
        session.id = completedMessage.session_id ?? null;
        session.name = question;
        onSessionCreated(session);
      }
    } catch (e) {
      console.error(e);
      session.messages[session.messages.length - 1].answer =
        "There was an error connecting to the server.";
    }
    scrollToBottom();
  }

  let scrollContainer: HTMLDivElement;
  let userScrolledUp = false;
  const scrollToBottom = () => {
    if (!userScrolledUp && scrollContainer) {
      scrollContainer.scrollTo({ top: scrollContainer.scrollHeight, behavior: "smooth" });
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
  class="relative h-full w-full"
  on:dragenter={(event) => {
    event.preventDefault();
    isDragging = true;
  }}
>
  <div
    class="flex h-full max-h-full flex-grow flex-col items-center justify-start overflow-y-auto pr-6"
    bind:this={scrollContainer}
    on:scroll={handleScroll}
  >
    {#if session.messages && session.messages.length > 0}
      {#each session.messages as message}
        <ChatMessage {message} />
      {/each}
    {:else}
      <div class="absolute inset-0 flex items-center justify-center text-stone-500">
        <div class="flex flex-col items-center gap-2">
          <IconSession size="large" class="text-stone-300" />

          <p class="text-center">
            Hi, I'm <span class="inline italic">{assistant.name}</span>!<br />Ask me a question to
            get started
          </p>
        </div>
      </div>
    {/if}
    <div class="flex-grow"></div>
    <div
      class="chatbox-gradient sticky bottom-0 left-0 right-0 flex w-full flex-col items-center justify-end gap-2 pb-4 pt-8"
    >
      <ChatInput {assistant} {askQuestion} />
    </div>
  </div>
  {#if isDragging}
    <ChatDragAndDrop bind:isDragging imagesAllowed={assistant.completion_model?.vision} />
  {/if}
</div>

<style lang="postcss">
  .chatbox-gradient {
    background: linear-gradient(0deg, rgb(255, 255, 255) 0%, rgba(0, 0, 0, 0) 80%),
      radial-gradient(
        120% 100px at center 120px,
        rgba(255, 255, 255, 0.75) 0%,
        rgba(0, 0, 0, 0) 80%
      );
  }
</style>
