<script>
  import { Page } from "$lib/components/layout";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { onMount } from "svelte";
  import AppsTable from "./AppsTable.svelte";
  import TemplateCreateApp from "$lib/features/templates/components/apps/TemplateCreateApp.svelte";
  import { createAppTemplateAdapter } from "$lib/features/templates/TemplateAdapter";
  import { initTemplateController } from "$lib/features/templates/TemplateController";
  import TemplateCreateAppHint from "$lib/features/templates/components/apps/TemplateCreateAppHint.svelte";
  export let data;

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  initTemplateController({
    adapter: createAppTemplateAdapter({
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
  <title>Intric.ai – {$currentSpace.personal ? "Personal" : $currentSpace.name} – Apps</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Apps"></Page.Title>
    {#if $currentSpace.hasPermission("create", "app")}
      <TemplateCreateApp></TemplateCreateApp>
    {/if}
  </Page.Header>
  <Page.Main>
    {#if $currentSpace.applications.apps.length < 1 && data.featureFlags.showTemplates && $currentSpace.hasPermission("create", "app")}
      <TemplateCreateAppHint></TemplateCreateAppHint>
    {:else}
      <AppsTable apps={$currentSpace.applications.apps}></AppsTable>
    {/if}
  </Page.Main>
</Page.Root>
