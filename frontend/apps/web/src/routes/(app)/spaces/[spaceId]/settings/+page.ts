// MIT License

export const load = async (event) => {
  const { intric } = await event.parent();

  const models = await intric.models.list();

  return models;
};
