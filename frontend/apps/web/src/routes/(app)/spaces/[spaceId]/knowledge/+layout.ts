export const load = async (event) => {
  const { intric } = await event.parent();

  const availableIntegrations = await intric.integrations.user.list();

  return { availableIntegrations };
};
