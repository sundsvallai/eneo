/* 
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

import { env } from "$env/dynamic/private";
import { loginWithMobilityguard } from "$lib/features/auth/oidc.server.js";
import { redirect } from "@sveltejs/kit";

export const load = async (event) => {
  const code = event.url.searchParams.get("code");
  const state = event.url.searchParams.get("state");

  let success = false;
  if (code && state) {
    try {
      if (state === "mobilityguard") {
        if (!env.MOBILITY_GUARD_AUTH) {
          redirect(302, "/login");
        }
        success = await loginWithMobilityguard(event.url.origin, code, event.cookies);
      }
    } catch (e) {
      alert(e);
    }
    if (success) {
      // TODO: Redirect to dashboard instead (once we have it)
      redirect(302, "/spaces/personal");
    }
  }

  redirect(302, "/login?message=oicderror");
};
