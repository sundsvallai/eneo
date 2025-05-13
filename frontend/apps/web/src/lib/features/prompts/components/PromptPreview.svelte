<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Button } from "@intric/ui";
  import { getPromptManager } from "../PromptManager";
  import dayjs from "dayjs";
  import relativeTime from "dayjs/plugin/relativeTime";
  import utc from "dayjs/plugin/utc";
  import MemberChip from "../../spaces/components/MemberChip.svelte";
  import EditPromptDescription from "./EditPromptDescription.svelte";

  dayjs.extend(relativeTime);
  dayjs.extend(utc);

  const {
    state: { previewedPrompt, showPromptVersionDialog },
    onPromptSelected
  } = getPromptManager();
</script>

<div class="flex flex-col gap-3.5">
  {#if $previewedPrompt}
    <section class="flex-grow">
      <div
        class="border-default bg-primary sticky top-0 flex items-center justify-between border-b px-4 py-2.5 font-medium backdrop-blur"
      >
        <h2 class="font-medium">
          <span class="sr-only">Previewing prompt created at</span>
          <span aria-hidden="true">Version:</span>
          {dayjs($previewedPrompt?.created_at).format("YYYY-MM-DD HH:mm")}
        </h2>
        <MemberChip member={$previewedPrompt.user}></MemberChip>
      </div>

      <div class="flex-grow overflow-y-auto p-8 whitespace-pre-wrap">
        {$previewedPrompt.text}
      </div>
    </section>

    <div class="flex flex-col gap-3">
      {#if $previewedPrompt.description}
        <div
          class="border-accent-stronger bg-accent-dimmer text-accent-stronger rounded-md border px-5 py-4"
        >
          {$previewedPrompt.description}
        </div>
      {/if}

      <div class=" flex items-end justify-between">
        {#key $previewedPrompt.id}
          <EditPromptDescription prompt={$previewedPrompt}></EditPromptDescription>
        {/key}

        <Button
          disabled={$previewedPrompt.is_selected ?? false}
          on:click={() => {
            $showPromptVersionDialog = false;
            onPromptSelected($previewedPrompt);
          }}
          variant="primary"
          >Restore this version
        </Button>
      </div>
    </div>
  {:else}
    <div class="text-secondary flex h-full w-full items-center justify-center">
      Please select a prompt
    </div>
  {/if}
</div>

<style lang="postcss">
  @reference "@intric/ui/styles";
  section {
    @apply border-stronger bg-primary overflow-auto rounded-md border border-b shadow-md;
  }
</style>
