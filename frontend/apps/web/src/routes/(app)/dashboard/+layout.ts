export const load = async (event) => {
  const { intric } = await event.parent();

  const dashboard = await intric.dashboard.list();

  return {
    spaces: dashboard.spaces.items.map((space) => space)
  };
};
