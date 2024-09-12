<script lang="ts">
  import type { Assistant, AssistantSession } from "@intric/intric-js";
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";
  import SelectSession from "./SelectSession.svelte";
  import DeleteSession from "./DeleteSession.svelte";

  import dayjs from "dayjs";
  import relativeTime from "dayjs/plugin/relativeTime";
  import utc from "dayjs/plugin/utc";
  dayjs.extend(relativeTime);
  dayjs.extend(utc);

  export let sessions: Omit<AssistantSession, "messages">[];
  export let assistant: Assistant;
  export let selectSession: (session: Omit<AssistantSession, "messages">) => void;
  export let refreshSessions: () => void;

  const table = Table.createWithResource(sessions);

  const viewModel = table.createViewModel([
    table.columnPrimary({
      header: "Name",
      value: (item) => item.name ?? "",
      cell: (item) => {
        return createRender(SelectSession, {
          session: item.value,
          selectSession
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
        return createRender(DeleteSession, {
          session: item.value,
          assistant,
          refreshSessions
        });
      }
    })
  ]);

  $: table.update(sessions);
</script>

<Table.Root {viewModel} resourceName="session" emptyMessage="No previous sessions found"
></Table.Root>
