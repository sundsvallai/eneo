<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { setAdminUserCtx } from "./ctx";
  import InviteUser from "./editor/InviteUser.svelte";
  import UserTable from "./UserTable.svelte";

  export let data;

  setAdminUserCtx({
    customRoles: data.customRoles,
    defaultRoles: data.defaultRoles,
    userGroups: data.userGroups
  });
</script>

<svelte:head>
  <title>Eneo.ai – Admin – Users</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Users"></Page.Title>
    <InviteUser></InviteUser>
  </Page.Header>
  <Page.Main>
    <UserTable users={data.users} />
  </Page.Main>
</Page.Root>
