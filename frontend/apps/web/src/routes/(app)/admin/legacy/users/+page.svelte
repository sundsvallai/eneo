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

  // We put roles and user groups into the context so we don't need to pass them manually
  // Loaded through layout so they will not be affected by `invalidate()`
  setAdminUserCtx(data);
</script>

<svelte:head>
  <title>Intric.ai – Admin – Users</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Users"></Page.Title>
    <UserEditor mode="create"></UserEditor>
  </Page.Header>
  <Page.Main>
    <UserTable users={data.users} />
  </Page.Main>
</Page.Root>
