import type { Intric } from "@intric/intric-js";
import type { PageLoad } from "./$types";

export const load: PageLoad = async (event) => {
  const { intric }: { intric: Intric } = await event.parent();
  const selectedAssistantId = event.params.assistantId;
  const selectedSessionId = event.params.sessionId;

  const loadSession = async () => {
    return selectedSessionId
      ? intric.assistants.getSession({
          assistant: { id: selectedAssistantId },
          session: { id: selectedSessionId }
        })
      : null;
  };

  event.depends("assistant:get");

  const [assistant, sessions, session] = await Promise.all([
    intric.assistants.get({ id: selectedAssistantId }),
    intric.assistants
      .listSessions({ id: selectedAssistantId })
      .then((sessions) => sessions.reverse()),
    loadSession()
  ]);

  return {
    assistant,
    sessions,
    session,
    selectedAssistantId
  };
};
