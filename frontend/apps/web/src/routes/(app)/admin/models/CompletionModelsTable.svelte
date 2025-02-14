<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import type { CompletionModel } from "@intric/intric-js";
  import { Table } from "@intric/ui";
  import { createRender } from "svelte-headless-table";
  import ModelEnabledSwitch from "./ModelEnableSwitch.svelte";
  import {
    default as ModelLabels,
    getLabels
  } from "$lib/features/ai-models/components/ModelLabels.svelte";
  import { modelOrgs } from "$lib/features/ai-models/components/ModelNameAndVendor.svelte";
  import ModelActions from "./ModelActions.svelte";
  import ModelCardDialog from "$lib/features/ai-models/components/ModelCardDialog.svelte";

  export let completionModels: CompletionModel[];
  const table = Table.createWithResource(completionModels);

  const viewModel = table.createViewModel([
    table.column({
      accessor: (model) => model,
      header: "Name",
      cell: (item) => {
        return createRender(ModelCardDialog, { model: item.value, includeTrigger: true });
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
        return createRender(ModelEnabledSwitch, { model: item.value });
      },
      plugins: {
        sort: {
          getSortValue(value) {
            return value.is_org_enabled ? 1 : 0;
          }
        }
      }
    }),

    table.column({
      accessor: (model) => model,
      header: "Details",
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

    table.columnActions({
      cell: (item) => {
        return createRender(ModelActions, { model: item.value });
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
