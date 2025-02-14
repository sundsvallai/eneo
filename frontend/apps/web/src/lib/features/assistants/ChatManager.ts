import { browser } from "$app/environment";
import { createContext } from "$lib/core/context";
import {
  type AssistantResponse,
  type AssistantSession,
  type Assistant,
  type Intric,
  type UploadedFile,
  IntricError,
  type Paginated
} from "@intric/intric-js";
import { get, writable, derived } from "svelte/store";
import { PAGINATION } from "$lib/core/constants";
import { waitFor } from "$lib/core/waitFor";

const [getChatManager, setChatManager] = createContext<ReturnType<typeof ChatManager>>(
  "Manages the state of an assistant's chat / sessions"
);

function initChatManager(data: ChatManagerParams) {
  const context = ChatManager(data);
  setChatManager(context);
  return context;
}

type Session = Omit<AssistantSession, "id" | "messages"> & {
  id: string | null;
  messages?: AssistantResponse[] | null;
};

type SessionHistoryEntry = Omit<AssistantSession, "messages">;

type ChatManagerParams = {
  /** The assistant you want to talk to */
  assistant: Assistant;
  /** Provide an initial session that should be displayed on creation – optional*/
  initialSession?: Promise<Session | null> | Session | null;
  /** Provide the session history of this assistant, with pagination – optional */
  history?: Promise<Paginated<SessionHistoryEntry>> | Paginated<SessionHistoryEntry>;
  intric: Intric;
};

function ChatManager(data: ChatManagerParams) {
  const { intric, assistant: initialAssistant } = data;

  const currentAssistant = writable<Assistant>(initialAssistant);
  const getAssistant = () => get(currentAssistant);
  const history = writable<SessionHistoryEntry[]>([]);
  const nextCursor = writable<string | null>(null);
  const totalSessions = writable<number>(0);

  waitFor(data.history, {
    onLoaded(initialHistory) {
      history.set(initialHistory.items);
      totalSessions.set(initialHistory.total_count);
      nextCursor.set(initialHistory.next_cursor ?? null);
    }
  });

  const currentSession = writable<Session>(emptySession());

  waitFor(data.initialSession, {
    onLoaded(initialSession) {
      currentSession.set(initialSession);
    }
  });

  const isAskingQuestion = writable<boolean>(false);

  function startNewSession() {
    currentSession.set(emptySession());
  }

  async function loadSession(session: { id: string }) {
    try {
      const newSession = await intric.assistants.getSession({ session, assistant: getAssistant() });
      currentSession.set(newSession);
      return newSession;
    } catch (e) {
      if (browser) alert(`Error while loading session ${session.id}`);
      console.error(e);
    }
  }

  async function deleteSession(session: { id: string }) {
    try {
      const deleted = await intric.assistants.deleteSession({ session, assistant: getAssistant() });
      history.update((history) => {
        return history.filter((session) => session.id !== deleted.id);
      });
      if (get(currentSession).id === deleted.id) {
        startNewSession();
      }
    } catch (e) {
      if (browser) alert(`Error while deleting session ${session.id}`);
      console.error(e);
    }
  }

  async function refreshHistory() {
    try {
      const updated = await intric.assistants.listSessions({
        assistant: getAssistant(),
        pagination: { limit: PAGINATION.PAGE_SIZE }
      });
      history.set(updated.items);
      nextCursor.set(updated.next_cursor ?? null);
      totalSessions.set(updated.total_count);
    } catch (e) {
      if (browser) alert(`Error when loading sessions for assistant ${getAssistant().id}`);
      console.error(e);
    }
  }

  async function loadMoreSessions(limit?: number) {
    try {
      const response = await intric.assistants.listSessions({
        assistant: getAssistant(),
        pagination: { limit: limit ?? PAGINATION.PAGE_SIZE, cursor: get(nextCursor) ?? undefined }
      });
      history.update(($history) => {
        $history.push(...response.items);
        return $history;
      });
      nextCursor.set(response.next_cursor ?? null);
      return response;
    } catch (error) {
      console.error("Error loading pagination", error);
    }
  }

  /**
   * Ask this assistant a question
   * @param abortController (optional) Pass in an AbortController to manually cancel the stream
   * @param scrollFn (optional) Will be called after a token is received, use it to e.g. scroll the answer into view
   */
  async function askQuestion(
    question: string,
    attachments: UploadedFile[] = [],
    abortController?: AbortController,
    scrollFn?: () => void
  ) {
    /** Will start out as null if this is an empty session  */
    let initialSessionId: null | string = null;

    isAskingQuestion.set(true);

    // Prepare current session to receive answer
    currentSession.update(($currentSession) => {
      initialSessionId = $currentSession.id;
      if (!$currentSession.messages) {
        $currentSession.messages = [];
      }
      $currentSession.messages.push({
        question,
        answer: "",
        references: [],
        id: "",
        files: attachments
      });
      return $currentSession;
    });

    scrollFn?.();

    let buffer = "";

    try {
      const message = await intric.assistants.ask({
        assistant: getAssistant(),
        session: { id: initialSessionId },
        question,
        files: attachments.map((fileRef) => ({ id: fileRef.id })),
        onAnswer: ({ answer, references, session_id }, controller) => {
          currentSession.update(($currentSession) => {
            if (initialSessionId === null && $currentSession.id === null) {
              initialSessionId = session_id ?? null;
              $currentSession.name = question;
              $currentSession.id = session_id ?? null;
            }

            // Check if we're receiving an answer for the current session
            if ($currentSession.id !== session_id) {
              controller.abort();
              return $currentSession;
            }

            // Check if we might receive a reference and dont show it immediately
            if (answer.includes("<") || buffer) {
              buffer += answer;
              if (isNotInref(buffer) || isCompleteInref(buffer)) {
                $currentSession.messages![$currentSession.messages!.length - 1].answer += buffer;
                buffer = "";
              }
            } else {
              $currentSession.messages![$currentSession.messages!.length - 1].answer += answer;
            }

            $currentSession.messages![$currentSession.messages!.length - 1].references = references;
            return $currentSession;
          });
          scrollFn?.();
        },
        abortController
      });
      currentSession.update(($currentSession) => {
        $currentSession.messages![$currentSession.messages!.length - 1] = message;
        return $currentSession;
      });
    } catch (error) {
      const streamAborted = error instanceof Error && error.message.includes("aborted");
      if (streamAborted) {
        // In that case nothing more to do, just return
        return;
      }

      let message = "We encountered an error processing your request.";
      if (error instanceof IntricError) {
        message += `\n\`\`\`\n${error.code}: "${error.getReadableMessage()}"\n\`\`\``;
      } else if (error instanceof Object && "message" in error && "name" in error) {
        message += `\n\`\`\`\n$"${error.name}: error.message}"\n\`\`\``;
      }

      currentSession.update(($currentSession) => {
        $currentSession.messages![$currentSession.messages!.length - 1].answer = message;
        return $currentSession;
      });

      console.error(error);
    } finally {
      isAskingQuestion.set(false);
      scrollFn?.();
    }

    refreshHistory();
  }

  function changeAssistant(newAssistant: Assistant) {
    const oldAssistant = getAssistant();
    currentAssistant.set(newAssistant);

    if (oldAssistant.id !== newAssistant.id) {
      refreshHistory();
      startNewSession();
    }
  }

  /** Call this to avoid re-loading history and sessions when re-running a page load */
  function reInit(data: ChatManagerParams) {
    currentAssistant.set(data.assistant);

    waitFor(data.initialSession, {
      onLoaded(initialSession) {
        currentSession.set(initialSession);
      },
      onNull() {
        currentSession.set(emptySession());
      }
    });

    waitFor(data.history, {
      onLoaded(initialHistory) {
        history.set(initialHistory.items);
        totalSessions.set(initialHistory.total_count);
        nextCursor.set(initialHistory.next_cursor ?? null);
      },
      onNull() {
        history.set([]);
        nextCursor.set(null);
        totalSessions.set(0);
      }
    });
  }

  return Object.freeze({
    state: {
      currentSession: {
        subscribe: currentSession.subscribe
      },
      history: { subscribe: history.subscribe },
      isAskingQuestion: { subscribe: isAskingQuestion.subscribe },
      assistant: { subscribe: currentAssistant.subscribe },
      hasMoreSessions: derived(nextCursor, ($cursor) => $cursor !== null),
      loadedSessions: derived(history, ($history) => $history.length),
      totalSessions: { subscribe: totalSessions.subscribe }
    },
    startNewSession,
    askQuestion,
    loadSession,
    deleteSession,
    changeAssistant,
    reInit,
    loadMoreSessions
  });
}

function emptySession(): Session {
  return {
    id: null,
    messages: [],
    name: "New session"
  };
}

const couldBeInref = (buffer: string): boolean => {
  // We assume that "<" can be anywhere in the buffer, but that there can only be one
  return "<inref".startsWith(buffer.slice(buffer.indexOf("<"), 5));
};
const isNotInref = (buffer: string): boolean => !couldBeInref(buffer);
const isCompleteInref = (buffer: string): boolean => couldBeInref(buffer) && buffer.includes(">");

export { initChatManager, getChatManager, type ChatManagerParams };
