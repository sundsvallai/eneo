<script lang="ts">
  import IconUpload from "$lib/components/icons/IconUpload.svelte";
  import type { AssistantResponse } from "@intric/intric-js";
  import { Markdown } from "@intric/ui";
  import { fly } from "svelte/transition";
  import References from "./References.svelte";

  export let message: AssistantResponse;
  let copiedTextElement: HTMLElement;
</script>

<div class="group/message flex w-full max-w-[74ch] flex-col gap-2 p-4">
  {#if message.files && message.files.length > 0}
    <div class="flex w-full items-center justify-end gap-2">
      {#each message.files as file}
        <div
          class="flex items-center gap-3.5 rounded-md border border-stone-200 py-1.5 pl-1.5 pr-6 hover:bg-stone-50"
        >
          <div
            class="flex h-12 w-12 items-center justify-center rounded-md border border-blue-700 bg-blue-600"
          >
            <IconUpload class="stroke-white" />
          </div>
          <div>
            <p class="">
              {file.name}
            </p>
            <p class="text-sm text-gray-500">
              {file.name.split(".")[file.name.split(".").length - 1].toUpperCase()}
            </p>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- animation needs to be outside if block, otherwise it will be re-triggered -->
  <div
    in:fly={{ y: 20 }}
    class="max-w-full self-end break-words rounded-xl rounded-br-none bg-stone-200"
  >
    {#if message.question}
      <div class="whitespace-pre-wrap px-8 py-4 text-lg">
        {message.question}
      </div>
    {/if}
  </div>

  <div class="prose prose-stone relative pt-6 text-lg prose-p:text-black">
    <Markdown.Highlighted source={message.answer} />

    <div class="absolute -left-3 top-6 flex -translate-x-full items-center gap-2">
      <span
        style="opacity: 0;"
        class="hidden text-sm text-blue-600 group-hover/message:block"
        bind:this={copiedTextElement}>Copied!</span
      >
      <button
        class="hidden h-7 w-7 items-center justify-center rounded-md bg-stone-100 text-stone-600 hover:bg-stone-800 hover:text-white group-hover/message:flex"
        on:click={() => {
          navigator.clipboard.writeText(message.answer);
          if (copiedTextElement) {
            copiedTextElement.style.opacity = "1";
            setTimeout(() => {
              copiedTextElement.style.opacity = "0";
            }, 2000);
          }
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="h-5 w-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M8.25 7.5V6.108c0-1.135.845-2.098 1.976-2.192.373-.03.748-.057 1.123-.08M15.75 18H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08M15.75 18.75v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5A3.375 3.375 0 0 0 6.375 7.5H5.25m11.9-3.664A2.251 2.251 0 0 0 15 2.25h-1.5a2.251 2.251 0 0 0-2.15 1.586m5.8 0c.065.21.1.433.1.664v.75h-6V4.5c0-.231.035-.454.1-.664M6.75 7.5H4.875c-.621 0-1.125.504-1.125 1.125v12c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V16.5a9 9 0 0 0-9-9Z"
          />
        </svg>
      </button>
    </div>
  </div>

  {#if message.references && message.references.length > 0}
    <References {message} />
  {/if}
</div>
