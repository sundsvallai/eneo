<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import CreateService from "./CreateService.svelte";
  import ServicesTable from "./ServicesTable.svelte";

  const {
    state: { currentSpace }
  } = getSpacesManager();
</script>

<svelte:head>
  <title>Eneo.ai – {$currentSpace.personal ? "Personal" : $currentSpace.name} – Services</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Services"></Page.Title>
    {#if $currentSpace.hasPermission("create", "service")}
      <CreateService></CreateService>
    {/if}
  </Page.Header>
  <Page.Main>
    <ServicesTable services={$currentSpace.applications.services}></ServicesTable>
  </Page.Main>
</Page.Root>
