export const load = async (event) => {
  const { intric } = await event.parent();

  const [securityClassifications, models] = await Promise.all([
    intric.securityClassifications.list(),
    intric.models.list()
  ]);

  return {
    securityClassifications,
    models
  };
};
