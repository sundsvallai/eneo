<script lang="ts">
  import type { AssistantResponse } from "@intric/intric-js";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
  import MessageQuestion from "./MessageQuestion.svelte";
  import MessageAnswer from "./MessageAnswer.svelte";
  import MessageFiles from "./MessageFiles.svelte";
  import MessageTools from "./MessageTools.svelte";

  export let message: AssistantResponse;
  export let isLast: boolean;
  export let isLoading: boolean;
</script>

<div class="group/message mx-auto flex w-full max-w-[71ch] flex-col gap-4">
  <MessageFiles files={message.files}></MessageFiles>
  <MessageQuestion contents={message.question} isAnimated={isLast && isLoading}></MessageQuestion>
  <div class="md:h-2"></div>
  <MessageAnswer contents={message.answer} references={message.references}></MessageAnswer>
  {#if isLoading && isLast}
    <IconLoadingSpinner class="animate-spin" />
  {:else}
    <MessageTools {message} {isLast}></MessageTools>
  {/if}
</div>
