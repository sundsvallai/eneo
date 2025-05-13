export const load = async (event) => {
  const { intric } = await event.parent();
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

  const [assistant, session] = await Promise.all([
    intric.assistants.get({ id: selectedAssistantId }),
    loadSession()
  ]);

  return {
    chatPartner: assistant,
    initialConversation: session
  };
};
