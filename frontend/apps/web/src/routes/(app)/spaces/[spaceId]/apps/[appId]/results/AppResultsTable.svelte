<script lang="ts">
  import { Table } from "@intric/ui";
  import type { App, AppRunSparse } from "@intric/intric-js";
  import { createRender } from "svelte-headless-table";
  import dayjs from "dayjs";
  import relativeTime from "dayjs/plugin/relativeTime";
  import utc from "dayjs/plugin/utc";
  import { getResultTitle } from "$lib/features/apps/getResultTitle";
  import ResultPrimaryCell from "./ResultPrimaryCell.svelte";
  import AppResultStatus from "$lib/features/apps/components/AppResultStatus.svelte";
  import ResultAction from "./ResultAction.svelte";

  dayjs.extend(relativeTime);
  dayjs.extend(utc);

  export let results: AppRunSparse[];
  export let app: App;

  const table = Table.createWithResource(results);

  function onResultDeleted(result: { id: string }) {
    results = results.filter((r) => r.id !== result.id);
  }

  const viewModel = table.createViewModel([
    table.columnPrimary({
      header: "Name",
      value: (item) => getResultTitle(item),
      cell: (item) => {
        return createRender(ResultPrimaryCell, {
          run: item.value,
          app
        });
      }
    }),
    table.column({
      header: "Status",
      accessor: (item) => item,
      cell: (item) => {
        return createRender(AppResultStatus, {
          run: item.value
        });
      }
    }),
    table.column({
      header: "Created",
      accessor: "created_at",
      cell: (item) => {
        return createRender(Table.FormattedCell, {
          value: dayjs(item.value).format("YYYY-MM-DD HH:mm"),
          monospaced: true
        });
      }
    }),

    table.columnActions({
      cell: (item) => {
        return createRender(ResultAction, {
          result: item.value,
          onResultDeleted
        });
      }
    })
  ]);

  $: table.update(results);
</script>

<Table.Root {viewModel} resourceName="result" emptyMessage="No previous results found"></Table.Root>
