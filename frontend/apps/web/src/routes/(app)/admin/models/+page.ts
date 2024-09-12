// MIT License

export const load = async (event) => {
  const { intric } = await event.parent();

  event.depends("admin:models:load");

  const models = await intric.models.list();

  return {
    models
  };
};
