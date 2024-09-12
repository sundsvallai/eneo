<script lang="ts">
  import type { AssistantSparse } from "@intric/intric-js";
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";
  import AssistantTile from "./AssistantTile.svelte";
  import IconAssistant from "$lib/components/icons/IconAssistant.svelte";
  import AssistantActions from "./AssistantActions.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";

  export let assistants: AssistantSparse[];
  const table = Table.createWithResource(assistants);

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
          link: `/spaces/${$currentSpace.routeId}/assistants/${item.value.id}`,
          icon: IconAssistant
        });
      }
    }),

    table.columnActions({
      cell: (item) => {
        return createRender(AssistantActions, {
          assistant: item.value
        });
      }
    }),

    table.columnCard({
      value: (item) => item.name,
      cell: (item) => {
        return createRender(AssistantTile, {
          assistant: item.value
        });
      }
    })
  ]);

  $: table.update(assistants);
</script>

<Table.Root
  {viewModel}
  resourceName="assistant"
  displayAs="cards"
  gapX={1.5}
  gapY={1.5}
  layout="grid"
></Table.Root>
