import { createZitadelClient } from "$lib/core/Zitadel";
import { createIntric, createIntricSocket } from "@intric/intric-js";

export const load = async (event) => {
  event.depends("global:state");
  const intric = createIntric({
    token: event.data.tokens.id_token,
    baseUrl: event.data.baseUrl!,
    fetch: event.fetch
  });

  let zitadelClient: ReturnType<typeof createZitadelClient> | null = null;
  if (event.data.authUrl && event.data.tokens.access_token) {
    zitadelClient = createZitadelClient(
      event.data.authUrl,
      event.data.tokens.access_token,
      event.fetch
    );
  }

  const intricSocket = createIntricSocket(
    {
      token: event.data.tokens.id_token,
      baseUrl: event.data.baseUrl!
    },
    {
      defaultSubscriptions: ["app_run_updates"]
    }
  );

  const getUserInfo = async () => {
    if (zitadelClient) {
      try {
        const [userInfo, usesIdp] = await Promise.all([
          zitadelClient.getUserInfo(),
          zitadelClient.getNumOfLinkedIdps().then((num) => num > 0)
        ]);
        return { ...userInfo, usesIdp };
      } catch (e) {
        console.error("Couldnt get user info, maybe URL not allowed?");
      }
    }
    return null;
  };

  const [userInfo, user, tenant, backendVersion, limits] = await Promise.all([
    getUserInfo(),
    intric.users.me(),
    intric.users.tenant(),
    intric.version.get(),
    intric.limits.list()
  ]);

  const versions = {
    frontend: event.data.frontendVersion,
    backend: backendVersion,
    client: intric.client.version,
    preview: event.data.previewEnv
  };

  return {
    intric,
    intricSocket,
    zitadelClient,
    user,
    userInfo: userInfo ?? {
      firstName: user.email,
      lastName: user.email,
      displayName: user.email,
      usesIdp: false
    },
    tenant,
    versions,
    limits,
    featureFlags: event.data.featureFlags,
    feedbackFormUrl: event.data.feedbackFormUrl,
    integrationRequestFormUrl: event.data.integrationRequestFormUrl
  };
};
