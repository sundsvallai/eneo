/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

export const load = async (event) => {
  const { intric } = await event.parent();

  const [roles, userGroups] = await Promise.all([intric.roles.list(), intric.userGroups.list()]);

  return {
    customRoles: roles.roles,
    defaultRoles: roles.predefined_roles,
    userGroups
  };
};
