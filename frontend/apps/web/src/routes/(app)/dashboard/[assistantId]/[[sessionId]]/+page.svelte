<script lang="ts">
  import { Button } from "@intric/ui";
  import { initChatManager } from "$lib/features/assistants/ChatManager.js";
  import { pushState } from "$app/navigation";
  import { page } from "$app/stores";
  import SessionView from "$lib/features/assistants/components/session/SessionView.svelte";
  import { fade, fly } from "svelte/transition";
  import { quadInOut } from "svelte/easing";

  export let data;

  const {
    state: { currentSession, assistant },
    loadSession,
    startNewSession,
    reInit
  } = initChatManager(data);

  // In the current dashboard config this will never run, as you can't open old sessions
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
  $: reInit(data);
</script>

<svelte:head>
  <title>Intric.ai – Dashboard – {data.assistant.name}</title>
</svelte:head>

<div class="outer flex w-full flex-col bg-primary">
  <div
    class="sticky top-0 flex items-center justify-between bg-primary px-3.5 py-3 backdrop-blur-md"
    in:fade={{ duration: 50 }}
  >
    <a href="/dashboard" class="flex max-w-[calc(100%_-_7rem)] flex-grow items-center rounded-lg">
      <span
        class="flex h-8 w-8 items-center justify-center rounded-lg border border-default hover:bg-hover-dimmer"
        >←</span
      >
      <h1
        in:fly|global={{
          x: -5,
          duration: parent ? 300 : 0,
          easing: quadInOut,
          opacity: 0.3
        }}
        class="truncate px-3 py-1 text-xl font-extrabold"
      >
        {$assistant.name}
      </h1>
    </a>
    <Button
      variant="primary"
      on:click={() => {
        startNewSession();
        pushState(`/dashboard/${data.assistant.id}?tab=chat`, {
          session: undefined,
          tab: "chat"
        });
      }}
      class="!rounded-lg !border-b-2 !border-[var(--color-ui-blue-700)] !px-5 !py-1"
      >New chat
    </Button>
  </div>

  <SessionView></SessionView>
</div>

<style>
  @media (display-mode: standalone) {
    .outer {
      background-color: var(--background-primary);
      overflow-y: auto;
      margin: 0 0.5rem;
      border-radius: 1rem;
      box-shadow: 0 4px 10px 0px rgba(0, 0, 0, 0.1);
      max-height: 100%;
    }
  }

  @container (min-width: 1000px) {
    .outer {
      margin: 1.5rem;
      border-radius: 1rem;
      box-shadow: 0 4px 10px 0px rgba(0, 0, 0, 0.1);
      max-width: 1400px;
      overflow: hidden;
    }
  }
</style>
