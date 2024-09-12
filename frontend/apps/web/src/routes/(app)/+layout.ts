import { createIntric } from "@intric/intric-js";

export const load = async (event) => {
  event.depends("global:state");

  const intric = createIntric({
    token: event.data.token,
    baseUrl: event.data.baseUrl!,
    fetch: event.fetch
  });

  const [user, tenant, backendVersion, limits] = await Promise.all([
    intric.users.me(),
    intric.users.tenant(),
    intric.version.get(),
    intric.limits.list()
  ]);

  const versions = {
    frontend: event.data.frontendVersion,
    backend: backendVersion,
    client: intric.client.version,
    preview: event.data.vercelEnv
  };

  return {
    intric,
    user,
    tenant,
    versions,
    limits
  };
};
