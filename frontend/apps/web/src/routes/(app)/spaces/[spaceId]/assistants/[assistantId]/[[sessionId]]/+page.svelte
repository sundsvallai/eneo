<script lang="ts">
  import { Page } from "$lib/components/layout";
  import HistoryTable from "$lib/features/assistants/components/history/HistoryTable.svelte";
  import QuestionsAboutQuestions from "./insights/QuestionsAboutQuestions.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { initChatManager } from "$lib/features/assistants/ChatManager.js";
  import SessionView from "$lib/features/assistants/components/session/SessionView.svelte";
  import { pushState } from "$app/navigation";
  import { page } from "$app/stores";
  import { Button } from "@intric/ui";
  import AssistantSwitcher from "$lib/features/assistants/components/switcher/AssistantSwitcher.svelte";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
  import { fade } from "svelte/transition";

  export let data;

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const {
    state: { currentSession, hasMoreSessions, loadedSessions, totalSessions },
    loadSession,
    startNewSession,
    changeAssistant,
    loadMoreSessions
  } = initChatManager(data);

  async function watchPageState(currentPage: { state: { session?: { id: string } } }) {
    if ("session" in currentPage.state && currentPage.state.session) {
      // When the user clicks the back button in the browser we will cycle
      // through the previous state values. When neccessary, we should load the
      // corresponding session.
      if ($currentSession.id !== currentPage.state.session.id)
        loadSession(currentPage.state.session);
    }
  }

  $: watchPageState($page);
  $: changeAssistant(data.assistant);
</script>

<svelte:head>
  <title
    >Intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – {data
      .assistant.name}</title
  >
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title truncate={true} parent={{ href: `/spaces/${$currentSpace.routeId}/assistants` }}>
      <AssistantSwitcher></AssistantSwitcher>
    </Page.Title>

    <Page.Tabbar>
      <Page.TabTrigger tab="chat">Chat</Page.TabTrigger>
      <Page.TabTrigger tab="history">History</Page.TabTrigger>
      <!-- TODO: Do we need a specific permission for this? -->
      {#if data.assistant.permissions?.includes("edit")}
        <Page.TabTrigger tab="insights">Insights</Page.TabTrigger>
      {/if}
    </Page.Tabbar>

    <Page.Flex>
      {#if data.assistant.permissions?.includes("edit")}
        <Button href="/spaces/{$currentSpace.routeId}/assistants/{data.assistant.id}/edit"
          >Edit</Button
        >
      {/if}
      <Button
        variant="primary"
        on:click={() => {
          startNewSession();
          pushState(`/spaces/${$currentSpace.routeId}/assistants/${data.assistant.id}?tab=chat`, {
            session: undefined,
            tab: "chat"
          });
        }}
        class="!line-clamp-1"
        >New conversation
      </Button>
    </Page.Flex>
  </Page.Header>

  <Page.Main>
    <Page.Tab id="chat">
      <SessionView></SessionView>
    </Page.Tab>
    <Page.Tab id="history">
      {#await data.history}
        <!-- TODO: This has some delay on it as the underlying table is delayed in updating its rows, so we cover it up during that time. -->
        <div
          class="absolute inset-0 z-[100] flex items-center justify-center bg-primary"
          out:fade={{ delay: 250, duration: 100 }}
        >
          <IconLoadingSpinner class="animate-spin"></IconLoadingSpinner>
        </div>
      {/await}
      <HistoryTable
        onSessionLoaded={(session) => {
          pushState(
            `/spaces/${$currentSpace.routeId}/assistants/${data.assistant.id}/${session.id}?tab=chat`,
            {
              session,
              tab: "chat"
            }
          );
        }}
        onSessionDeleted={() => {
          pushState(
            `/spaces/${$currentSpace.routeId}/assistants/${data.assistant.id}?tab=history`,
            {
              session: undefined,
              tab: "history"
            }
          );
        }}
      />

      <div class="flex-col pb-12 pt-8 text-secondary">
        <div class="flex flex-col items-center justify-center gap-2">
          {#if $hasMoreSessions}
            <Button
              variant="primary-outlined"
              on:click={() => loadMoreSessions()}
              aria-label="Load more conversations"
            >
              Load more conversations</Button
            >
            <p role="status" aria-live="polite">
              Loaded {$loadedSessions}/{$totalSessions} conversations
            </p>
          {:else if $totalSessions > 0}
            <p role="status" aria-live="polite">
              Loaded all {$totalSessions} conversations.
            </p>
          {/if}
        </div>
      </div>
    </Page.Tab>

    <Page.Tab id="insights">
      <QuestionsAboutQuestions assistant={data.assistant} />
    </Page.Tab>
  </Page.Main>
</Page.Root>
