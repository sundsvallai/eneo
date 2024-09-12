<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { onMount } from "svelte";
  import AssistantsTable from "./AssistantsTable.svelte";
  import CreateAssistant from "./CreateAssistant.svelte";

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  onMount(() => {
    refreshCurrentSpace();
  });
</script>

<svelte:head>
  <title>Intric.ai – {$currentSpace.personal ? "Personal" : $currentSpace.name} – Assistants</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title>Assistants</Page.Title>
    {#if $currentSpace.hasPermission("create", "assistant")}
      <CreateAssistant></CreateAssistant>
    {/if}
  </Page.Header>

  <Page.Main>
    <AssistantsTable assistants={$currentSpace.applications.assistants}></AssistantsTable>
  </Page.Main>
</Page.Root>
