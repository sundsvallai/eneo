<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Page } from "$lib/components/layout";

  import IconAssistants from "$lib/components/icons/IconAssistants.svelte";
  import IconSession from "$lib/components/icons/IconSession.svelte";
  import IconQuestion from "$lib/components/icons/IconQuestion.svelte";

  import InteractiveGraph from "./InteractiveGraph.svelte";
  import TenantAssistantTable from "./TenantAssistantTable.svelte";
  import LoadingSpinner from "$lib/components/icons/LoadingSpinner.svelte";

  export let data;

  let selectedTab: Page.ValueState;
</script>

<svelte:head>
  <title>Intric.ai – Admin – Insights</title>
</svelte:head>

<Page.Root bind:selectedTab>
  <Page.Header>
    <Page.Title>Insights</Page.Title>
    <Page.Tabbar>
      <Page.TabTrigger tab="overview">Usage</Page.TabTrigger>
      <Page.TabTrigger tab="assistants">Assistants</Page.TabTrigger>
    </Page.Tabbar>
  </Page.Header>
  <Page.Main>
    <Page.Tab id="overview">
      {#if $selectedTab === "overview"}
        <div class="h-full max-h-[700px] min-h-[450px] max-w-[1200px] p-4 pl-0 pr-4">
          <div
            class="relativ flex h-full w-full items-stretch overflow-clip rounded-lg border border-stone-300 shadow"
          >
            {#await data.data}
              <div class="flex h-full w-full items-center justify-center">
                <div class="flex flex-col items-center justify-center gap-2 pt-3">
                  <LoadingSpinner />
                  Loading data...
                </div>
              </div>
            {:then loadedData}
              <InteractiveGraph data={loadedData} timeframe={data.timeframe}></InteractiveGraph>

              <div class="flex flex-grow flex-col border-l bg-stone-50">
                <div class="flex h-1/3 flex-col justify-between border-b p-6">
                  <div class="flex gap-2">
                    <IconAssistants></IconAssistants>
                    Assistants created
                  </div>
                  <span class="self-end text-[2.75rem] font-medium"
                    >{loadedData.assistants.length}</span
                  >
                </div>

                <div class="flex h-1/3 flex-col justify-between border-b p-6">
                  <div class="flex gap-2">
                    <IconSession></IconSession>
                    Conversations started
                  </div>
                  <span class="self-end text-[2.75rem] font-medium"
                    >{loadedData.sessions.length}</span
                  >
                </div>

                <div class="flex h-1/3 flex-col justify-between p-6">
                  <div class="flex gap-2">
                    <IconQuestion></IconQuestion>
                    Questions asked
                  </div>
                  <span class="self-end text-[2.75rem] font-medium"
                    >{loadedData.questions.length}</span
                  >
                </div>
              </div>
            {/await}
          </div>
        </div>
      {/if}
    </Page.Tab>
    <Page.Tab id="assistants">
      <TenantAssistantTable assistants={data.assistants} />
    </Page.Tab>
  </Page.Main>
</Page.Root>
