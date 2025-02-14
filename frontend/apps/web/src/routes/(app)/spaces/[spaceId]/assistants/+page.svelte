<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { onMount } from "svelte";
  import AssistantsTable from "./AssistantsTable.svelte";
  import TemplateCreateAssistant from "$lib/features/templates/components/assistants/TemplateCreateAssistant.svelte";
  import TemplateCreateAssistantHint from "$lib/features/templates/components/assistants/TemplateCreateAssistantHint.svelte";
  import { initTemplateController } from "$lib/features/templates/TemplateController";
  import { createAssistantTemplateAdapter } from "$lib/features/templates/TemplateAdapter";

  export let data;

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  initTemplateController({
    adapter: createAssistantTemplateAdapter({
      intric: data.intric,
      currentSpaceId: $currentSpace.id
    }),
    allTemplates: data.allTemplates
  });

  onMount(() => {
    refreshCurrentSpace();
  });
</script>

<svelte:head>
  <title>Intric.ai – {$currentSpace.personal ? "Personal" : $currentSpace.name} – Assistants</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Assistants"></Page.Title>
    {#if $currentSpace.hasPermission("create", "assistant")}
      <TemplateCreateAssistant></TemplateCreateAssistant>
    {/if}
  </Page.Header>

  <Page.Main>
    {#if $currentSpace.applications.assistants.length < 1 && data.featureFlags.showTemplates && $currentSpace.hasPermission("create", "assistant")}
      <TemplateCreateAssistantHint></TemplateCreateAssistantHint>
    {:else}
      <AssistantsTable assistants={$currentSpace.applications.assistants}></AssistantsTable>
    {/if}
  </Page.Main>
</Page.Root>
