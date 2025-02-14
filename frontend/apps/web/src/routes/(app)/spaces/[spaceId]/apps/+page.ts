export const load = async (event) => {
  const { intric } = await event.parent();
  const allTemplates = await intric.templates.list({ filter: "apps" });

  return {
    allTemplates
  };
};
