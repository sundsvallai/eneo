<script lang="ts">
  import type { CrawlRun } from "@intric/intric-js";
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";

  import dayjs from "dayjs";
  import relativeTime from "dayjs/plugin/relativeTime";
  import utc from "dayjs/plugin/utc";
  import CrawlResultCell from "./CrawlResultCell.svelte";
  dayjs.extend(relativeTime);
  dayjs.extend(utc);

  export let runs: CrawlRun[];
  const table = Table.createWithResource(runs);

  const viewModel = table.createViewModel([
    table.column({
      accessor: "created_at",
      header: "Started",
      cell: (item) => {
        return createRender(Table.FormattedCell, {
          value: dayjs(item.value).format("YYYY-MM-DD HH:mm"),
          monospaced: true
        });
      }
    }),

    table.column({
      accessor: "status",
      header: "Status",
      cell: (item) => {
        return createRender(Table.FormattedCell, {
          value: item.value ?? "No status found",
          class: "capitalize"
        });
      }
    }),

    table.column({
      accessor: (item) => item,
      header: "Results",
      cell: (item) => {
        return createRender(CrawlResultCell, {
          crawl: item.value
        });
      },
      plugins: { sort: { disable: true } }
    }),

    table.column({
      accessor: (item) => item,
      header: "Duration",
      plugins: {
        sort: { disable: true },
        tableFilter: {
          getFilterValue() {
            return "";
          }
        }
      },
      cell: (item) => {
        const started = dayjs(item.value.created_at);
        let value = `Started ${dayjs().to(started)}`;

        if (item.value.finished_at) {
          const finished = dayjs(item.value.finished_at);
          value = started.to(finished, true);
        }

        return createRender(Table.FormattedCell, {
          value
        });
      }
    })
  ]);

  $: table.update(runs);
</script>

<Table.Root
  {viewModel}
  filter
  emptyMessage="This website has not been crawled before"
  resourceName="crawl"
></Table.Root>
