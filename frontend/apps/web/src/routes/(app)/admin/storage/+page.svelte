<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Page, Settings } from "$lib/components/layout";
  import StorageOverviewBar from "./StorageOverviewBar.svelte";
  import StorageTable from "./StorageTable.svelte";

  export let data;
</script>

<svelte:head>
  <title>Intric.ai – Admin – Storage</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Storage"></Page.Title>
  </Page.Header>
  <Page.Main>
    <Settings.Page>
      <Settings.Group title="Overview">
        <StorageOverviewBar storageStats={data.storageStats}></StorageOverviewBar>
      </Settings.Group>
      <Settings.Group title="Details">
        <Settings.Row
          title="Public Spaces"
          description="See this organisation's public spaces and their storage use."
          fullWidth
        >
          <StorageTable spaces={data.spaces} />
        </Settings.Row>
      </Settings.Group>
    </Settings.Page>
  </Page.Main>
</Page.Root>
