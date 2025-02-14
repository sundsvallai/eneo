export const load = async (event) => {
  const { intric } = await event.parent();
  const app = await intric.apps.get({ id: event.params.appId });
  return { app };
};
