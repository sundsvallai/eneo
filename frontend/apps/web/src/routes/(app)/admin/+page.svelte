<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Page, Settings } from "$lib/components/layout/index.js";
  import { getAppContext } from "$lib/core/AppContext.js";
  import StorageOverviewBar from "./storage/StorageOverviewBar.svelte";

  const { tenant } = getAppContext();
  export let data;
</script>

<svelte:head>
  <title>Intric.ai - {tenant.display_name}</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Organisation"></Page.Title>
  </Page.Header>
  <Page.Main>
    <Settings.Page>
      <Settings.Group title="Storage">
        <StorageOverviewBar storageStats={data.storageStats}></StorageOverviewBar>
      </Settings.Group>
    </Settings.Page>
  </Page.Main>
</Page.Root>
