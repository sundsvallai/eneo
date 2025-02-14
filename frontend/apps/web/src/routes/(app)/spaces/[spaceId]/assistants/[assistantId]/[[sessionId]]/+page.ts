import type { Intric } from "@intric/intric-js";
import type { PageLoad } from "./$types";
import { PAGINATION } from "$lib/core/constants";

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

  return {
    assistant: await intric.assistants.get({ id: selectedAssistantId }),
    history: intric.assistants.listSessions({
      assistant: { id: selectedAssistantId },
      pagination: { limit: PAGINATION.PAGE_SIZE }
    }),
    initialSession: loadSession(),
    selectedAssistantId
  };
};
