<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<!-- Needs to be a svelte 4 component for compatibility reasons with the table -->

<script lang="ts">
  import type { ConversationSparse } from "@intric/intric-js";
  import { getInsightsService } from "../InsightsService.svelte";
  import { Button } from "@intric/ui";

  const insights = getInsightsService();
  export let conversation: ConversationSparse;
</script>

<div class="flex w-full items-center justify-start">
  <Button
    on:click={() => insights.loadConversationPreview(conversation)}
    class="max-w-full"
    data-selected={insights.previewedConversation?.id !== conversation.id}
  >
    <div
      class="bg-accent-dimmer absolute inset-0 z-[-1] hidden mix-blend-multiply"
      class:hidden={insights.previewedConversation?.id !== conversation.id}
    ></div>

    <span class="truncate overflow-ellipsis">
      {conversation.name}
    </span>
  </Button>
</div>
