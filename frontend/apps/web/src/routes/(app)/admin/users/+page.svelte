<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { setAdminUserCtx } from "./ctx";
  import UserEditor from "./editor/UserEditor.svelte";
  import UserTable from "./UserTable.svelte";

  export let data;

  setAdminUserCtx({
    customRoles: data.customRoles,
    defaultRoles: data.defaultRoles,
    userGroups: data.userGroups
  });
</script>

<svelte:head>
  <title>Intric.ai – Admin – Users</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title>Users</Page.Title>
    <UserEditor mode="create"></UserEditor>
  </Page.Header>
  <Page.Main>
    <UserTable users={data.users} />
  </Page.Main>
</Page.Root>
