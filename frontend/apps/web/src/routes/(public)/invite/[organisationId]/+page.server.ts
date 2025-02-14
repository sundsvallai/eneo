import { getZitadelLink } from "$lib/features/auth/zitadel.server.js";

export const load = async (event) => {
  let zitadelLink: string | undefined = undefined;
  if (event.locals.featureFlags.newAuth) {
    zitadelLink = await getZitadelLink(event, {
      registerUser: true,
      orgId: event.params.organisationId
    });
  }

  return {
    zitadelLink
  };
};
