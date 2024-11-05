<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Page, Sidebar } from "$lib/components/layout";
  import QuestionRow from "./QuestionRow.svelte";
  import { Button, Input } from "@intric/ui";
  import ChatView from "./ChatView.svelte";
  import { page } from "$app/stores";

  export let data;

  let questions = data.questions;
  let period: number = data.period;
  let includeFollowups: boolean = data.includeFollowups;

  let updating = false;
  async function updateQuestions() {
    questions = await data.intric.analytics.listQuestions({
      assistant: { id: $page.params.assistantId },
      options: { period, includeFollowups }
    });
  }
</script>

<svelte:head>
  <title>Intric.ai – Admin – {data.assistant.name} – Insights</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title parent={{ title: "Insights", href: "/admin/insights?tab=assistants" }}>
      {data.assistant.name}
    </Page.Title>
    <Page.Tabbar>
      <Page.TabTrigger tab="chat">Analyse</Page.TabTrigger>
      <Page.TabTrigger tab="questions">Question history</Page.TabTrigger>
    </Page.Tabbar>
  </Page.Header>

  <Page.Main>
    <Page.Tab id="chat">
      <ChatView assistant={data.assistant} {includeFollowups} {period}></ChatView>
    </Page.Tab>
    <Page.Tab id="questions">
      {#if questions && questions.length > 0}
        <ul class="flex flex-col">
          {#each questions as message}
            <QuestionRow {message}></QuestionRow>
          {/each}
        </ul>
      {:else}
        <div class="absolute inset-0 flex items-center justify-center text-stone-500">
          <div class="flex flex-col items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1"
              stroke="currentColor"
              class="h-24 w-24 text-stone-200"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 0 0-1.883 2.542l.857 6a2.25 2.25 0 0 0 2.227 1.932H19.05a2.25 2.25 0 0 0 2.227-1.932l.857-6a2.25 2.25 0 0 0-1.883-2.542m-16.5 0V6A2.25 2.25 0 0 1 6 3.75h3.879a1.5 1.5 0 0 1 1.06.44l2.122 2.12a1.5 1.5 0 0 0 1.06.44H18A2.25 2.25 0 0 1 20.25 9v.776"
              />
            </svg>

            No Questions found.
          </div>
        </div>
      {/if}
    </Page.Tab>
  </Page.Main>
</Page.Root>

<Sidebar.Root>
  <Sidebar.List>
    <Sidebar.Trigger label="Filter" panel="filter">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="h-6 w-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z"
        />
      </svg>
    </Sidebar.Trigger>
  </Sidebar.List>
  <Sidebar.Panel id="filter" title="Filter">
    <div class="flex min-h-full flex-grow flex-col justify-start">
      <Input.Number
        bind:value={period}
        min={1}
        max={30}
        class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50"
        >Timeframe (days):</Input.Number
      >

      <Input.Switch
        bind:value={includeFollowups}
        class="border-b border-stone-100 px-6 py-4 hover:bg-stone-50"
        >Include follow-up questions</Input.Switch
      >

      <div class="flex-grow"></div>

      <div class="sticky bottom-0 flex justify-end bg-gradient-to-t from-white to-transparent p-4">
        <Button variant="primary" on:click={updateQuestions} disabled={updating} class="w-[140px]"
          >{#if updating}Loading...{:else}Update{/if}</Button
        >
      </div>
    </div></Sidebar.Panel
  >
</Sidebar.Root>
