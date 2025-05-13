<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import Message from "$lib/features/chat/components/conversation/Message.svelte";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
  import { getInsightsService } from "../InsightsService.svelte";

  const insights = getInsightsService();
  const conversation = $derived(insights.previewedConversation);
</script>

<div class="flex flex-col gap-3.5">
  {#if insights.loadConversationPreview.isLoading}
    <div class="text-secondary flex h-full w-full items-center justify-center">
      <IconLoadingSpinner class="animate-spin"></IconLoadingSpinner>
    </div>
  {:else if conversation && conversation.messages.length > 0}
    <section class="flex-grow">
      <div class="flex flex-grow flex-col gap-2 p-4 md:p-8">
        {#each conversation.messages as message, idx (idx)}
          <Message {message} isLoading={false} isLast={idx === conversation.messages.length - 1}
          ></Message>
        {/each}
      </div>
    </section>
  {:else if conversation}
    <div class="text-secondary flex h-full w-full items-center justify-center">
      This conversation does not have any messages.
    </div>
  {:else}
    <div class="text-secondary flex h-full w-full items-center justify-center">
      Please select a conversation.
    </div>
  {/if}
</div>

<style lang="postcss">
  @reference "@intric/ui/styles";
  section {
    @apply border-stronger bg-primary overflow-auto rounded-md border border-b shadow-md;
  }
</style>
