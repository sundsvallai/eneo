/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

export const load = async (event) => {
  const { intric } = await event.parent();

  event.depends("admin:users:load");

  const users = await intric.users.list({ includeDetails: true });

  return {
    users
  };
};
