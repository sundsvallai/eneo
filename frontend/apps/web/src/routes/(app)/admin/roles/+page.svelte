<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Page } from "$lib/components/layout/index.js";
  import RoleEditor from "./RoleEditor.svelte";
  import RolesTable from "./RolesTable.svelte";

  export let data;
</script>

<svelte:head>
  <title>Intric.ai – Admin – Roles</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title>Roles</Page.Title>
    <Page.Tabbar>
      <Page.TabTrigger tab="custom_roles">Custom roles</Page.TabTrigger>
      <Page.TabTrigger tab="default_roles">Default roles</Page.TabTrigger>
    </Page.Tabbar>
    <RoleEditor mode="create" permissions={data.permissions}></RoleEditor>
  </Page.Header>

  <Page.Main>
    <Page.Tab id="custom_roles">
      <RolesTable roles={data.customRoles} permissions={data.permissions} />
    </Page.Tab>
    <Page.Tab id="default_roles">
      {#if data.defaultRoles.length > 0}
        <RolesTable roles={data.defaultRoles} permissions={data.permissions} editabel={false} />
      {/if}
    </Page.Tab>
  </Page.Main>
</Page.Root>
