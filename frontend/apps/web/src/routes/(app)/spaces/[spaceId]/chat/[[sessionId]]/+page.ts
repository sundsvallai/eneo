import { PAGINATION } from "$lib/core/constants";

export const load = async (event) => {
  const { intric, currentSpace } = await event.parent();
  const selectedAssistantId = currentSpace.default_assistant.id;
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
    assistant: currentSpace.default_assistant,
    history: intric.assistants.listSessions({
      assistant: { id: selectedAssistantId },
      pagination: { limit: PAGINATION.PAGE_SIZE }
    }),
    initialSession: loadSession(),
    selectedAssistantId
  };
};
