<script lang="ts">
  import type { InfoBlob } from "@intric/intric-js";
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";
  import BlobPreview from "$lib/features/knowledge/components/BlobPreview.svelte";
  import BlobActions from "./BlobActions.svelte";
  import { formatBytes } from "$lib/core/formatting/formatBytes";

  export let blobs: InfoBlob[];
  export let canEdit: boolean;
  const table = Table.createWithResource(blobs);

  const viewModel = table.createViewModel([
    table.columnPrimary({
      header: "Name",
      value: (item) => item.metadata.title ?? "",
      cell: (item) => {
        return createRender(BlobPreview, {
          blob: item.value,
          isTableView: true
        });
      }
    }),

    table.column({
      header: "Size",
      accessor: (item) => item,
      cell: (item) => formatBytes(item.value.metadata.size),
      plugins: {
        sort: { getSortValue: (item) => item.metadata.size }
      }
    }),

    table.columnActions({
      cell: (item) => {
        return createRender(BlobActions, {
          blob: item.value,
          canEdit
        });
      }
    })
  ]);

  $: table.update(blobs);
</script>

<Table.Root
  {viewModel}
  filter
  resourceName="file"
  emptyMessage="You do not have any files uploaded yet"
></Table.Root>
