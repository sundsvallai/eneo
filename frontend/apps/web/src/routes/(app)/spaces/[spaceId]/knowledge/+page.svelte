<script lang="ts">
  import { Page } from "$lib/components/layout";
  import CollectionEditor from "./collections/CollectionEditor.svelte";
  import CollectionTable from "./collections/CollectionTable.svelte";
  import WebsiteEditor from "./websites/WebsiteEditor.svelte";
  import WebsiteTable from "./websites/WebsiteTable.svelte";
  import type { Writable } from "svelte/store";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  export let data;

  const {
    state: { currentSpace }
  } = getSpacesManager();

  let selectedTab: Writable<string> & { get: () => string };
</script>

<svelte:head>
  <title
    >Intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – Knowledge</title
  >
</svelte:head>

<Page.Root bind:selectedTab>
  <Page.Header>
    <Page.Title>Knowledge</Page.Title>
    <Page.Tabbar>
      {#if $currentSpace.hasPermission("read", "collection")}
        <Page.TabTrigger tab="collections">Collections</Page.TabTrigger>
      {/if}
      {#if $currentSpace.hasPermission("read", "website")}
        <Page.TabTrigger tab="websites">Websites</Page.TabTrigger>
      {/if}
    </Page.Tabbar>
    <div class="flex-grow"></div>
    <Page.Flex>
      {#if $selectedTab === "collections" && $currentSpace.hasPermission("create", "collection")}
        <CollectionEditor mode="create" collection={undefined}></CollectionEditor>
      {:else if $selectedTab === "websites" && $currentSpace.hasPermission("create", "website")}
        <WebsiteEditor mode="create"></WebsiteEditor>
      {/if}
    </Page.Flex>
  </Page.Header>
  <Page.Main>
    {#if $currentSpace.hasPermission("read", "collection")}
      <Page.Tab id="collections">
        <CollectionTable></CollectionTable>
      </Page.Tab>
    {/if}
    {#if $currentSpace.hasPermission("read", "website")}
      <Page.Tab id="websites">
        <WebsiteTable></WebsiteTable>
      </Page.Tab>
    {/if}
  </Page.Main>
</Page.Root>
