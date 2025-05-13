/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

export const load = async (event) => {
  const { intric } = await event.parent();

  event.depends("admin:models:load");

  const [securityClassifications, models] = await Promise.all([
    intric.securityClassifications.list(),
    intric.models.list()
  ]);

  return {
    securityClassifications,
    models
  };
};
