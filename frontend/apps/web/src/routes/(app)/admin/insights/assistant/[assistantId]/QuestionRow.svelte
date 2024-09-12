<!-- MIT License -->

<script lang="ts">
  import IconQuestion from "$lib/components/icons/IconQuestion.svelte";
  import { getIntric } from "$lib/core/Intric";
  import type { AssistantResponse } from "@intric/intric-js";
  import { Button, Dialog, Markdown } from "@intric/ui";

  export let message: AssistantResponse & { id: string };

  const intric = getIntric();

  let loggingDetails: string;

  let loadingLog = false;
  async function loadLog() {
    if (!loggingDetails) {
      loadingLog = true;
      try {
        loggingDetails = JSON.stringify(await intric.logging.get(message), null, 2);
      } catch (e: unknown) {
        loggingDetails = JSON.stringify(message, null, 2);
      }
      loadingLog = false;
    }
    return true;
  }

  let isOpen: Dialog.OpenState;
</script>

<li
  class="flex h-16 items-center gap-2 border-b border-stone-200 py-2 pl-0.5 pr-4 hover:bg-stone-50"
>
  <div class="flex max-w-[80%] gap-3 border border-transparent px-1">
    <IconQuestion class="min-w-6 text-stone-300" />
    <span class="line-clamp-1">
      {message.question}
    </span>
  </div>

  <span class="flex-grow"></span>

  <Dialog.Root bind:isOpen>
    <Button
      on:click={() => {
        $isOpen = true;
        loadLog();
      }}
      variant="outlined"
      >Show details
    </Button>
    <Dialog.Content wide>
      <Dialog.Title>Details for "{message.question}"</Dialog.Title>
      <Dialog.Description hidden>Details for message with id {message.id}</Dialog.Description>
      {#if loadingLog}
        Loading...
      {:else}
        <Markdown.Code source={loggingDetails} class="max-h-[60vh]" />
      {/if}
      <Dialog.Controls let:close>
        <Button variant="primary" is={close}>Done</Button>
      </Dialog.Controls>
    </Dialog.Content>
  </Dialog.Root>
</li>
