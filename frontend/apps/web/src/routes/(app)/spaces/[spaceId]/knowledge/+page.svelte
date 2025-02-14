<script lang="ts">
  import { Page } from "$lib/components/layout";
  import CollectionEditor from "./collections/CollectionEditor.svelte";
  import CollectionTable from "./collections/CollectionTable.svelte";
  import WebsiteEditor from "./websites/WebsiteEditor.svelte";
  import WebsiteTable from "./websites/WebsiteTable.svelte";
  import type { Writable } from "svelte/store";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { Button } from "@intric/ui";
  import { IconLinkExternal } from "@intric/icons/link-external";
  export let data;

  const {
    state: { currentSpace }
  } = getSpacesManager();

  let selectedTab: Writable<string> & { get: () => string };
  let showIntegrationsNotice = data.integrationRequestFormUrl !== undefined;
</script>

<svelte:head>
  <title
    >Intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – Knowledge</title
  >
</svelte:head>

<Page.Root bind:selectedTab>
  <Page.Header>
    <Page.Title title="Knowledge"></Page.Title>
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
        {#if showIntegrationsNotice}
          <div class="hidden border-b border-dimmer py-3 pr-3 lg:block">
            <div
              class="label-neutral flex items-center gap-8 rounded-lg border border-label-default bg-label-dimmer px-4 py-3 text-label-stronger shadow"
            >
              <div class="flex flex-col">
                <span class="font-mono text-xs uppercase">coming soon</span>
                <span class="text-xl font-extrabold">Integrations</span>
              </div>
              <p class="-mt-[0.1rem] max-w-[85ch] pl-6 leading-[1.3rem]">
                You'll soon be able to directly connect intric to your most important knowledge
                sources, such as Sitevision and Sharepoint. <a
                  target="_blank"
                  rel="noreferrer"
                  class="inline items-center gap-1 underline hover:bg-label-stronger hover:text-label-dimmer"
                  href={data.integrationRequestFormUrl}
                  >Leave feedback or request an integration
                </a>
                <IconLinkExternal class="-mt-0.5 inline" size="sm"></IconLinkExternal>
              </p>
              <div class="flex-grow"></div>
              <Button
                variant="outlined"
                class="min-w-24"
                on:click={() => {
                  showIntegrationsNotice = false;
                }}>Dismiss</Button
              >
            </div>
          </div>
        {/if}
        <WebsiteTable></WebsiteTable>
      </Page.Tab>
    {/if}
  </Page.Main>
</Page.Root>
