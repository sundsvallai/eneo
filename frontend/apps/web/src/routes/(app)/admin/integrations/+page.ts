export const load = async (event) => {
  const { intric } = await event.parent();

  const tenantIntegrations = await intric.integrations.tenant.list();

  return { tenantIntegrations };
};
