<script lang="ts">
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";
  import AppTile from "./AppTile.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import type { AppSparse } from "@intric/intric-js";
  import { IconApp } from "@intric/icons/app";
  import AppActions from "./AppActions.svelte";

  export let apps: AppSparse[];
  const table = Table.createWithResource(apps);

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const viewModel = table.createViewModel([
    table.columnPrimary({
      header: "Name",
      value: (item) => item.name,
      cell: (item) => {
        return createRender(Table.PrimaryCell, {
          label: item.value.name,
          link: `/spaces/${$currentSpace.routeId}/apps/${item.value.id}`,
          icon: IconApp
        });
      }
    }),

    table.columnActions({
      cell: (item) => {
        return createRender(AppActions, {
          app: item.value
        });
      }
    }),

    table.columnCard({
      value: (item) => item.name,
      cell: (item) => {
        return createRender(AppTile, {
          app: item.value
        });
      }
    })
  ]);

  $: table.update(apps);
</script>

<Table.Root {viewModel} resourceName="app" displayAs="cards" gapX={1.5} gapY={1.5} layout="grid">
  <Table.Group></Table.Group>
</Table.Root>
