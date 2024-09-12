<!-- MIT License -->

<script lang="ts">
  import type { CompletionModel } from "@intric/intric-js";
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";
  import ModelEnabledSwitch from "./ModelEnableSwitch.svelte";
  import {
    default as ModelLabels,
    getLabels
  } from "$lib/features/ai-models/components/ModelLabels.svelte";
  import ModelTile from "./ModelTile.svelte";
  import ModelNameAndVendor, {
    modelOrgs
  } from "$lib/features/ai-models/components/ModelNameAndVendor.svelte";

  export let completionModels: CompletionModel[];
  const table = Table.createWithResource(completionModels);

  const viewModel = table.createViewModel([
    table.column({
      accessor: (model) => model,
      header: "Name",
      cell: (item) => {
        return createRender(ModelNameAndVendor, { model: item.value });
      },
      plugins: {
        sort: {
          getSortValue(value) {
            return value.nickname;
          }
        },
        tableFilter: {
          getFilterValue(value) {
            return `${value.nickname} ${value.org}`;
          }
        }
      }
    }),
    table.column({ accessor: "name", header: "Model" }),
    table.column({
      accessor: (model) => model,
      header: "Enabled",
      cell: (item) => {
        return createRender(ModelEnabledSwitch, { model: item.value, modeltype: "completion" });
      },
      plugins: {
        sort: {
          getSortValue(value) {
            return value.can_access ? 1 : 0;
          }
        }
      }
    }),
    table.column({
      accessor: (model) => model,
      header: "Labels",
      cell: (item) => {
        return createRender(ModelLabels, { model: item.value });
      },
      plugins: {
        sort: {
          disable: true
        },
        tableFilter: {
          getFilterValue(value) {
            const labels = getLabels(value).flatMap((label) => {
              return label.label;
            });
            return labels.join(" ");
          }
        }
      }
    }),
    table.columnCard({
      value: (item) => item.name,
      cell: (item) => {
        return createRender(ModelTile, {
          model: item.value,
          modeltype: "completion"
        });
      }
    })
  ]);

  function createOrgFilter(org: string | null | undefined) {
    return function (model: CompletionModel) {
      return model.org === org;
    };
  }

  $: table.update(completionModels);
</script>

<Table.Root {viewModel} resourceName="model" displayAs="list">
  {#each Object.entries(modelOrgs) as [org]}
    <Table.Group filterFn={createOrgFilter(org)} title={org} />
  {/each}
</Table.Root>
