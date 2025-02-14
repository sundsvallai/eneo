<script lang="ts">
  import { Page } from "$lib/components/layout";
  import HistoryTable from "$lib/features/assistants/components/history/HistoryTable.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { initChatManager } from "$lib/features/assistants/ChatManager.js";
  import SessionView from "$lib/features/assistants/components/session/SessionView.svelte";
  import { pushState } from "$app/navigation";
  import { page } from "$app/stores";
  import { Button } from "@intric/ui";
  import DefaultAssistantModelSwitcher from "$lib/features/assistants/components/switcher/DefaultAssistantModelSwitcher.svelte";
  import { getAppContext } from "$lib/core/AppContext.js";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
  import { fade } from "svelte/transition";

  export let data;

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const {
    state: { userInfo }
  } = getAppContext();

  const {
    state: { currentSession, hasMoreSessions, loadedSessions, totalSessions },
    loadSession,
    startNewSession,
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
</script>

<svelte:head>
  <title>Intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name}</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title truncate={true} title="Personal assistant"></Page.Title>

    <Page.Tabbar>
      <Page.TabTrigger tab="chat">Chat</Page.TabTrigger>
      <Page.TabTrigger tab="history">History</Page.TabTrigger>
    </Page.Tabbar>

    <Page.Flex>
      <DefaultAssistantModelSwitcher></DefaultAssistantModelSwitcher>
      <Button
        variant="primary"
        on:click={() => {
          startNewSession();
          pushState(`/spaces/${$currentSpace.routeId}/chat?tab=chat`, {
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
      <SessionView>
        <div class="max-w-[640px]">
          <div class="relative">
            <h3 class="b-1 text-2xl font-extrabold">Hi, {$userInfo.firstName}!</h3>
            <p class="max-w-[50ch] pr-20 pt-2 text-secondary">
              Welcome to intric. I'm your personal assistant and ready to help. Ask me a question to
              get started.
            </p>
          </div>
        </div>
      </SessionView>
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
          pushState(`/spaces/${$currentSpace.routeId}/chat/${session.id}?tab=chat`, {
            session,
            tab: "chat"
          });
        }}
        onSessionDeleted={() => {
          pushState(`/spaces/${$currentSpace.routeId}/chat?tab=history`, {
            session: undefined,
            tab: "history"
          });
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
  </Page.Main>
</Page.Root>
