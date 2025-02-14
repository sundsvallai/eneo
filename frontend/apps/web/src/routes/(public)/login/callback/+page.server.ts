import { DEFAULT_LANDING_PAGE } from "$lib/core/constants";
import { decodeState, type LoginStateParam } from "$lib/features/auth/auth.server.js";
import { LoginError } from "$lib/features/auth/LoginError.js";
import {
  clearMobilityguardCookie,
  loginWithMobilityguard
} from "$lib/features/auth/mobilityguard.server";
import { clearZitadelCookie, loginWithZitadel } from "$lib/features/auth/zitadel.server";
import { redirect } from "@sveltejs/kit";

export const load = async (event) => {
  const code = event.url.searchParams.get("code");
  const state = event.url.searchParams.get("state");

  if (!code) {
    return redirect(302, "/login?message=no_code_received");
  }

  if (!state) {
    return redirect(302, "/login?message=no_state_received");
  }

  let success = false;
  let errorInfo = "";
  const decodedState = decodeState<LoginStateParam>(state);
  const redirectUrl = decodedState?.next ?? DEFAULT_LANDING_PAGE;

  try {
    if (decodedState?.loginMethod === "mobilityguard") {
      success = await loginWithMobilityguard(event, code);
    }

    if (decodedState?.loginMethod === "zitadel") {
      success = await loginWithZitadel(event, code);
    }
  } catch (e) {
    if (e instanceof LoginError) {
      errorInfo = e.getErrorShortCode();
    }
  } finally {
    clearMobilityguardCookie(event.cookies);
    clearZitadelCookie(event.cookies);
  }

  if (success) {
    redirect(302, `/${redirectUrl.slice(1)}`);
  }

  redirect(302, `/login/failed?message=${decodedState?.loginMethod}_login_error&info=${errorInfo}`);
};
