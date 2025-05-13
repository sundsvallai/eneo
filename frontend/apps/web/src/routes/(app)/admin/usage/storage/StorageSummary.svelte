<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Settings } from "$lib/components/layout";
  import type { StorageSpaceList, StorageUsageSummary } from "@intric/intric-js";
  import StorageOverviewBar from "./StorageOverviewBar.svelte";
  import StorageTable from "./StorageTable.svelte";

  type Props = {
    spaces: StorageSpaceList[];
    storageStats: StorageUsageSummary;
  };

  const { spaces, storageStats }: Props = $props();
</script>

<Settings.Page>
  <Settings.Group title="Overview">
    <StorageOverviewBar {storageStats}></StorageOverviewBar>
  </Settings.Group>
  <Settings.Group title="Details">
    <Settings.Row
      title="Public Spaces"
      description="See this organisation's public spaces and their storage use."
      fullWidth
    >
      <StorageTable {spaces} />
    </Settings.Row>
  </Settings.Group>
</Settings.Page>
