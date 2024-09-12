<script lang="ts">
  import { Button, Input, Markdown } from "@intric/ui";
  import { fade } from "svelte/transition";
  import type { Assistant } from "@intric/intric-js";
  import LoadingSpinner from "$lib/components/icons/LoadingSpinner.svelte";
  import { getIntric } from "$lib/core/Intric";

  const intric = getIntric();

  export let assistant: Assistant;

  let includeFollowups: boolean;
  let period: number = 30;

  let question = "";
  let loadingAnswer = false;

  const NOT_ANSWERED = "_NO_QUESTION_ASKED_";
  let message = { question: "", answer: NOT_ANSWERED };

  async function askQuestion() {
    if (period > 30 || question === "") {
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
          period
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

<div
  class="sticky top-[30%] flex flex-col items-center justify-center gap-6 p-8 transition-all duration-700"
  style="top: {message.answer === NOT_ANSWERED ? '40%' : '0'}"
>
  <form class="sticky top-8 flex w-full max-w-[62ch] flex-col gap-2.5">
    <div
      class="flex w-full items-end justify-center gap-0.5 overflow-clip rounded-lg border border-stone-300 bg-stone-100 p-0.5 shadow-lg"
    >
      <textarea
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
        class="relative min-h-10 flex-grow resize-none overflow-y-auto rounded-md border border-stone-300 px-4 py-2 text-lg ring-stone-300 hover:border-stone-400 hover:ring-2"
      ></textarea>
      <button
        disabled={loadingAnswer}
        type="submit"
        on:click={askQuestion}
        class="rounded-lg border border-stone-100 bg-stone-100 p-2 text-lg hover:bg-stone-300"
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
    </div>
    <div class="flex justify-center gap-4">
      <div class="flex items-center gap-2">
        <label for="period_number">Timeframe (days):</label>
        <input
          type="number"
          bind:value={period}
          name="period_number"
          id="period_number"
          max="30"
          min="1"
          class="rounded-md border border-stone-300 p-1 pl-2"
        />
      </div>
      <div class="w-[1px] bg-stone-200"></div>
      <Input.Switch bind:value={includeFollowups}>Include follow-ups</Input.Switch>
    </div>
  </form>
  {#if message.answer === NOT_ANSWERED}
    <p class="text-center text-stone-400">
      Discover what users wanted to know from <span class="italic">{assistant.name}</span>.<br />Ask
      a question about the conversation history to get started.
    </p>
  {:else if message.answer !== ""}
    <div
      in:fade={{ duration: 300 }}
      class="prose prose-stone w-full rounded-lg border border-stone-200 px-8 py-4 text-lg prose-p:text-black"
    >
      <Markdown.Highlighted source={message.answer} />
    </div>
    {#if !loadingAnswer}
      <div transition:fade={{ delay: 400, duration: 400 }}>
        <Button
          variant="outlined"
          on:click={() => {
            message.answer = NOT_ANSWERED;
          }}>New question</Button
        >
      </div>
    {/if}
  {/if}
</div>
