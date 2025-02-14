export const load = async (event) => {
  const { intric } = await event.parent();
  const assistant = await intric.assistants.get({ id: event.params.assistantId });
  return { assistant };
};
