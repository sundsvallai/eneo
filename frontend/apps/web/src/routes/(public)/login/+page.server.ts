import { env } from "$env/dynamic/private";
import { loginUser } from "$lib/features/auth/auth.server.js";
import { getMobilityguardLink } from "$lib/features/auth/oidc.server.js";
import { redirect, fail, type Actions } from "@sveltejs/kit";

export const actions: Actions = {
  login: async ({ cookies, request }) => {
    const data = await request.formData();
    const username = data.get("email")?.toString() ?? null;
    const password = data.get("password")?.toString() ?? null;
    const next = data.get("next")?.toString() ?? null;

    if (username && password) {
      const success = await loginUser(cookies, username, password);

      if (success) {
        if (next) {
          redirect(302, `/${next.slice(1)}`);
        }
        // TODO: Redirect to dashboard instead (once we have it)
        redirect(302, "/spaces/personal");
      }
    }

    return fail(400, { failed: true });
  }
};

/* 
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/
export const load = async (event) => {
  // If user is logged in already: forward to base url, as login doesn't make sense
  if (event.locals.user.isLoggedIn) {
    redirect(302, "/");
  }

  let mobilityguardLink = undefined;
  if (env.MOBILITY_GUARD_AUTH) {
    mobilityguardLink = await getMobilityguardLink(event.url.origin, event.cookies);
  }

  return {
    mobilityguardLink
  };
};
