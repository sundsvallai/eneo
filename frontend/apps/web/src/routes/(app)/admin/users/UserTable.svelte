<!-- MIT License -->

<script lang="ts">
  import type { Group, Role, User } from "@intric/intric-js";
  import { Table, Label } from "@intric/ui";
  import UserActions from "./UserActions.svelte";
  import { createRender } from "svelte-headless-table";

  export let users: User[];
  const table = Table.createWithResource(users);

  const viewModel = table.createViewModel([
    table.column({ accessor: "username", header: "Username" }),
    // table.column({ accessor: "email", header: "Email" }),
    table.column({
      accessor: (user) => user,
      header: "Roles",
      cell: (item) => {
        const roles = item.value.roles?.concat(item.value.predefined_roles ?? []) ?? [];
        const content: { label: string; color: Label.LabelColor }[] = roles.map((group) => {
          return { label: group.name, color: "blue" };
        });
        return createRender(Label.List, { content });
      },
      plugins: {
        sort: {
          disable: true
        },
        tableFilter: {
          getFilterValue(value) {
            const roles = [...value.roles, ...value.predefined_roles];
            return roles.map((role: Role) => role.name).join(" ");
          }
        }
      }
    }),
    table.column({
      accessor: (user) => user,
      header: "Groups",
      cell: (item) => {
        const content: { label: string; color: Label.LabelColor }[] = item.value.user_groups.map(
          (group) => {
            return { label: group.name, color: "blue" };
          }
        );
        return createRender(Label.List, { content });
      },
      plugins: {
        sort: {
          disable: true
        },
        tableFilter: {
          getFilterValue(value) {
            const groups = value.user_groups ?? [];
            return groups.map((group: Group) => group.name).join(" ");
          }
        }
      }
    }),
    table.column({ accessor: "used_tokens", header: "Used tokens" }),
    table.columnActions({
      cell: (item) => {
        return createRender(UserActions, { user: item.value });
      }
    })
  ]);

  $: table.update(users);
</script>

<Table.Root {viewModel} resourceName="user"></Table.Root>
