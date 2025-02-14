import { dev } from "$app/environment";
import { DASHBOARD_URL } from "$lib/core/constants";
import { detectMobile } from "$lib/core/detectMobile";
import { getFeatureFlags } from "$lib/core/flags.server";
import { authenticateUser, clearFrontendCookies } from "$lib/features/auth/auth.server";
import { IntricError, type IntricErrorCode } from "@intric/intric-js";
import { redirect, type HandleServerError } from "@sveltejs/kit";

function routeRequiresLogin(route: { id: string | null }): boolean {
  const routeIsPublic = route.id?.includes("(public)") ?? false;
  return !routeIsPublic;
}

export const handle = async ({ event, resolve }) => {
  // Clear authentication cookies if the 'clear_cookies' URL parameter is present
  if (event.url.searchParams.get("clear_cookies")) {
    clearFrontendCookies(event);
  }

  const tokens = authenticateUser(event);
  const isLoggedIn = tokens.id_token != undefined;

  if (routeRequiresLogin(event.route)) {
    if (!isLoggedIn) {
      const redirectUrl = encodeURIComponent(event.url.pathname + event.url.search);
      redirect(302, `/login?next=${redirectUrl}`);
    }

    const isDashboard = event.url.pathname.startsWith("/dashboard");

    if (!isDashboard) {
      const userAgent = event.request.headers.get("user-agent");
      const isMobileOrTablet = userAgent ? detectMobile(userAgent) : false;
      if (isMobileOrTablet) {
        redirect(302, DASHBOARD_URL);
      }
    }
  }

  event.locals.id_token = tokens.id_token ?? null;
  event.locals.access_token = tokens.access_token ?? null;
  event.locals.featureFlags = getFeatureFlags();

  return resolve(event);
};

export const handleError: HandleServerError = async ({ error, status, message }) => {
  let code: IntricErrorCode = 0;
  if (error instanceof IntricError) {
    status = error.status;
    message = error.getReadableMessage();
    code = error.code;
  }

  if (dev) {
    console.error("server error", error);
  }

  return {
    status,
    message,
    code
  };
};
