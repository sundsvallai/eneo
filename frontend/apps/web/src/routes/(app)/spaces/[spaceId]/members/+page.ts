// MIT License

export const load = async (event) => {
  const { intric } = await event.parent();

  const users = await intric.users.list();

  return {
    users
  };
};
