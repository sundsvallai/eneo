<script lang="ts">
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";
  import HistoryActions from "./HistoryActions.svelte";

  import dayjs from "dayjs";
  import relativeTime from "dayjs/plugin/relativeTime";
  import utc from "dayjs/plugin/utc";
  dayjs.extend(relativeTime);
  dayjs.extend(utc);

  import { getChatManager } from "../../ChatManager";
  import type { AssistantSession } from "@intric/intric-js";

  export let onSessionLoaded: ((session: AssistantSession) => void) | undefined = undefined;
  export let onSessionDeleted: ((session: AssistantSession) => void) | undefined = undefined;

  const {
    state: { history },
    loadSession
  } = getChatManager();

  const table = Table.createWithStore(history);

  const viewModel = table.createViewModel([
    table.columnPrimary({
      header: "Name",
      value: (item) => item.name ?? "",
      cell: (item) => {
        return createRender(Table.ButtonCell, {
          label: item.value.name,
          async onclick() {
            const loaded = await loadSession(item.value);
            if (loaded && onSessionLoaded) {
              onSessionLoaded(loaded);
            }
          }
        });
      },
      sortable: false
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
        return createRender(HistoryActions, {
          session: item.value,
          onSessionDeleted
        });
      }
    })
  ]);
</script>

<Table.Root {viewModel} resourceName="session" emptyMessage="No previous sessions found"
></Table.Root>
