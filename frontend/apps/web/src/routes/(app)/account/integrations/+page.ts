export const load = async (event) => {
  const { intric } = await event.parent();

  const myIntegrations = await intric.integrations.user.list();

  return { myIntegrations };
};
