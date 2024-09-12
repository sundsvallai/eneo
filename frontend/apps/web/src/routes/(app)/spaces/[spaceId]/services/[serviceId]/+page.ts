export const load = async (event) => {
  const { intric } = await event.parent();
  const selectedServiceId = event.params.serviceId;

  event.depends("service:get");

  const service = await intric.services.get({ id: selectedServiceId });

  return { service, selectedServiceId };
};
