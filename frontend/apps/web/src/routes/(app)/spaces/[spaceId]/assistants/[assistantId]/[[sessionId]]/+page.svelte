<script lang="ts">
  import { Page } from "$lib/components/layout";
  import EditAssistant from "./EditAssistant.svelte";
  import ChatView from "./chat/ChatView.svelte";
  import { Button } from "@intric/ui";
  import type { AssistantResponse, AssistantSession } from "@intric/intric-js";
  import { pushState } from "$app/navigation";
  import { page } from "$app/stores";
  import { tick } from "svelte";
  import HistoryTable from "./history/HistoryTable.svelte";
  import QuestionsAboutQuestions from "./insights/QuestionsAboutQuestions.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";

  export let data;
  const intric = data.intric;
  const {
    state: { currentSpace }
  } = getSpacesManager();

  let sessions = data.sessions;
  type Session = Omit<AssistantSession, "created_at" | "updated_at" | "id" | "messages"> & {
    id: string | null;
    messages: AssistantResponse[];
  };
  let session: Session = getNewSession();

  function getNewSession() {
    return {
      id: null,
      messages: [],
      name: "Empty session"
    };
  }

  async function selectSession(session: Omit<AssistantSession, "messages">) {
    const selectedSession = await intric.assistants.getSession({
      assistant: data.assistant,
      session
    });
    pushState(
      `/spaces/${$currentSpace.routeId}/assistants/${data.assistant.id}/${selectedSession.id}?tab=chat`,
      {
        session: selectedSession,
        tab: "chat"
      }
    );
  }

  async function sessionCreated(session: Session) {
    refreshSessions();
    pushState(
      `/spaces/${$currentSpace.routeId}/assistants/${data.assistant.id}/${session.id}?tab=chat`,
      {
        session,
        tab: "chat"
      } as { session: AssistantSession; tab: string }
    );
  }

  async function refreshSessions() {
    sessions = (await intric.assistants.listSessions(data.assistant)).reverse();
  }

  async function watchPageState() {
    let newSession: Session | null = null;

    if ("session" in $page.state) {
      // Check if we have set a session on the state prop
      newSession = $page.state.session as Session;
    } else {
      // If no session override is set we check if we got one from the route
      newSession = data.session as Session;
    }

    // Update the session after the next tick
    await tick();
    session = newSession ?? getNewSession();
  }

  $: $page, watchPageState();
</script>

<svelte:head>
  <title
    >Intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – {data
      .assistant.name}</title
  >
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title
      parent={{ title: "Assistants", href: `/spaces/${$currentSpace.routeId}/assistants` }}
      >{data.assistant.name}</Page.Title
    >
    <Button
      variant="primary"
      on:click={() => {
        pushState(`/spaces/${$currentSpace.routeId}/assistants/${data.assistant.id}?tab=chat`, {
          session: undefined,
          tab: "chat"
        });
      }}
      class="!line-clamp-1"
      >New conversation
    </Button>
  </Page.Header>

  <Page.LegacyTabbar>
    <Page.Flex>
      <Page.LegacyTabTrigger tab="chat" label="Chat with {data.assistant.name}"
        >Chat</Page.LegacyTabTrigger
      >
      <Page.LegacyTabTrigger tab="history">History</Page.LegacyTabTrigger>
      <Page.LegacyTabTrigger tab="insights">Insights</Page.LegacyTabTrigger>
    </Page.Flex>
    <Page.Flex>
      <Page.LegacyTabTrigger tab="edit">Settings</Page.LegacyTabTrigger>
    </Page.Flex>
  </Page.LegacyTabbar>

  <Page.Main>
    <Page.Tab id="chat">
      <ChatView assistant={data.assistant} {session} onSessionCreated={sessionCreated}></ChatView>
    </Page.Tab>
    <Page.Tab id="history">
      <HistoryTable assistant={data.assistant} {sessions} {selectSession} {refreshSessions} />
    </Page.Tab>
    <Page.Tab id="insights">
      <QuestionsAboutQuestions assistant={data.assistant} />
    </Page.Tab>
    <Page.Tab id="edit">
      <EditAssistant assistant={data.assistant} />
    </Page.Tab>
  </Page.Main>
</Page.Root>
