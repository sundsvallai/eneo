<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Page } from "$lib/components/layout";
  import UserGroupEditor from "./UserGroupEditor.svelte";
  import UserGroupTable from "./UserGroupTable.svelte";

  export let data;
</script>

<svelte:head>
  <title>Eneo.ai – Admin – User Groups</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="User Groups"></Page.Title>
    <UserGroupEditor mode="create"></UserGroupEditor>
  </Page.Header>
  <Page.Main>
    <UserGroupTable userGroups={data.userGroups} />
  </Page.Main>
</Page.Root>
