import { env } from "$env/dynamic/private";
import { DEFAULT_LANDING_PAGE } from "$lib/core/constants";
import { loginWithIntric } from "$lib/features/auth/intric.server";
import { getMobilityguardLink } from "$lib/features/auth/mobilityguard.server";
import { getZitadelLink } from "$lib/features/auth/zitadel.server";
import { redirect, fail, type Actions } from "@sveltejs/kit";

export const actions: Actions = {
  login: async ({ request }) => {
    const data = await request.formData();
    const username = data.get("email")?.toString() ?? null;
    const password = data.get("password")?.toString() ?? null;
    const next = data.get("next")?.toString() ?? null;
    const redirectUrl = next ? decodeURIComponent(next) : DEFAULT_LANDING_PAGE;

    if (username && password) {
      const success = await loginWithIntric(username, password);

      if (success) {
        redirect(302, `/${redirectUrl.slice(1)}`);
      }
    }

    return fail(400, { failed: true });
  }
};

export const load = async (event) => {
  let zitadelLink: string | undefined = undefined;
  let mobilityguardLink: string | undefined = undefined;

  // If user is logged in already: forward to base url, as login doesn't make sense
  if (event.locals.id_token) {
    redirect(302, DEFAULT_LANDING_PAGE);
  }

  if (event.locals.featureFlags.newAuth) {
    zitadelLink = await getZitadelLink(event);
  }

  if (env.MOBILITY_GUARD_AUTH) {
    mobilityguardLink = await getMobilityguardLink(event);
  }

  return {
    mobilityguardLink,
    zitadelLink
  };
};
