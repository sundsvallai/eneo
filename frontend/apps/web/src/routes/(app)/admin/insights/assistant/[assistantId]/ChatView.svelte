<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
  import { IconEnter } from "@intric/icons/enter";
  import { Button, Markdown } from "@intric/ui";
  import { fade } from "svelte/transition";
  import { getIntric } from "$lib/core/Intric";
  import type { Assistant } from "@intric/intric-js";
  import type { CalendarDate } from "@internationalized/date";

  const intric = getIntric();

  export let assistant: Assistant;
  export let includeFollowups: boolean;
  export let timeframe: { start: CalendarDate; end: CalendarDate };

  let question = "";
  let loadingAnswer = false;

  const NOT_ANSWERED = "_NO_QUESTION_ASKED_";
  let message = { question: "", answer: NOT_ANSWERED };

  async function askQuestion() {
    if (question === "") {
      return;
    }

    loadingAnswer = true;

    message.question = question;
    message.answer = "";
    question = "";
    textarea.style.height = "auto";

    try {
      const { answer } = await intric.analytics.ask({
        assistant: { id: assistant.id },
        options: {
          includeFollowups,
          start: timeframe.start.toString(),
          end: timeframe.end.toString()
        },
        question: message.question,
        onAnswer: (token) => {
          message.answer += token;
        }
      });
      message.answer = answer;
    } catch (e) {
      console.error(e);
      message.answer = "There was an error connecting to the server.";
    }
    loadingAnswer = false;
  }

  let textarea: HTMLTextAreaElement;
</script>

<div class="absolute inset-0 flex flex-col items-center justify-center transition-all">
  <form
    class="sticky top-0 z-10 flex w-full flex-col items-center gap-4 bg-primary py-8 transition-all"
    aria-labelledby="insights_description"
  >
    <div
      class="flex w-full max-w-[62ch] items-end justify-center gap-1 overflow-clip rounded-lg border border-default bg-primary p-1 shadow-lg"
    >
      <textarea
        aria-label="Ask a question about what this assistant has been asked previously"
        placeholder="Ask about insights..."
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
            if (!loadingAnswer) {
              askQuestion();
            }
          }
        }}
        required
        name="question"
        id="question"
        rows="1"
        class="relative min-h-10 flex-grow resize-none overflow-y-auto rounded-md bg-primary px-4 py-2 text-lg ring-default placeholder:text-secondary hover:border-strongest hover:ring-2"
      ></textarea>
      <button
        disabled={loadingAnswer}
        type="submit"
        aria-label="Submit your question"
        on:click={askQuestion}
        class="flex h-11 w-11 items-center justify-center rounded-lg bg-secondary p-2 text-lg hover:bg-hover-stronger"
      >
        {#if loadingAnswer}
          <IconLoadingSpinner class="animate-spin" />
        {:else}
          <IconEnter />
        {/if}
      </button>
    </div>
  </form>

  {#if message.answer === NOT_ANSWERED}
    <p class="text-center text-secondary transition-all" id="insights_description">
      Discover what users wanted to know from <span class="italic">{assistant.name}</span>.<br />Ask
      a question about the conversation history to get started.
    </p>
  {:else if message.answer !== ""}
    <div
      in:fade={{ duration: 300 }}
      class="prose overflow-y-auto rounded-lg border border-default px-8 py-4 text-lg"
      aria-live="polite"
    >
      <Markdown source={message.answer} />
    </div>

    <div transition:fade={{ delay: 400, duration: 400 }}>
      <Button
        variant="outlined"
        class="my-4"
        on:click={() => {
          message.answer = NOT_ANSWERED;
        }}>New questions</Button
      >
    </div>
  {/if}
</div>
