<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Table } from "@intric/ui";
  import UserActions from "./UserGroupActions.svelte";
  import { createRender } from "svelte-headless-table";
  import type { UserGroup } from "@intric/intric-js";

  export let userGroups: UserGroup[];

  const table = Table.createWithResource(userGroups);

  const viewModel = table.createViewModel([
    table.column({ accessor: "name", header: "Name" }),
    table.columnActions({
      cell: (item) => {
        return createRender(UserActions, { userGroup: item.value });
      }
    })
  ]);

  $: table.update(userGroups);
</script>

<Table.Root {viewModel} resourceName="user group"></Table.Root>
