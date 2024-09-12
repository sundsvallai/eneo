<script lang="ts">
  import { invalidate } from "$app/navigation";
  import { Page } from "$lib/components/layout";
  import CrawlRunsTable from "./CrawlRunsTable.svelte";
  import { onMount } from "svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import BlobTable from "../../collections/[collectionId]/BlobTable.svelte";

  export let data;

  onMount(() => {
    const interval = setInterval(() => {
      invalidate("crawlruns:list");
    }, 30 * 1000);

    return () => clearInterval(interval);
  });

  const {
    state: { currentSpace }
  } = getSpacesManager();
</script>

<svelte:head>
  <title
    >Intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – Crawls for {data
      .website.name}</title
  >
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title
      parent={{
        title: "Knowledge",
        href: `/spaces/${$currentSpace.routeId}/knowledge?tab=websites`
      }}>{data.website.name}</Page.Title
    >
    <Page.Tabbar>
      <Page.TabTrigger tab="crawls">Crawls</Page.TabTrigger>
      <Page.TabTrigger tab="blobs">Indexed content</Page.TabTrigger>
    </Page.Tabbar>
  </Page.Header>
  <Page.Main>
    <Page.Tab id="crawls">
      <CrawlRunsTable runs={data.crawlRuns} />
    </Page.Tab>
    <Page.Tab id="blobs">
      <BlobTable blobs={data.infoBlobs} canEdit={false}></BlobTable>
    </Page.Tab>
  </Page.Main>
</Page.Root>
