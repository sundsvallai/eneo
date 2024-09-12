<!-- MIT License -->

<script lang="ts">
  import IconAssistant from "$lib/components/icons/IconAssistant.svelte";
  import type { Assistant } from "@intric/intric-js";
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";

  export let assistants: Assistant[];
  const table = Table.createWithResource(assistants);

  const viewModel = table.createViewModel([
    table.columnPrimary({
      header: "Name",
      value: (item) => item.name,
      cell: (item) => {
        return createRender(Table.PrimaryCell, {
          label: `${item.value.name} (Space: ${item.value.space_id})`,
          link: `/admin/insights/assistant/${item.value.id}`,
          icon: IconAssistant
        });
      }
    }),
    table.column({
      header: "Logging",
      accessor: "logging_enabled",
      cell: (item) => (item.value ? "Enabled" : "–"),
      plugins: {
        sort: { getSortValue: (item) => item.logging_enabled ?? 0 }
      }
    })
  ]);

  $: table.update(assistants);
</script>

<Table.Root {viewModel} emptyMessage="assistant"></Table.Root>
