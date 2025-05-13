import { redirect } from "@sveltejs/kit";

export const load = async (event) => {
  if (!event.locals.id_token) {
    // This should already have happend in the handle hook
    const redirectUrl = event.url.pathname + event.url.search;
    redirect(302, `/login?next=${encodeURIComponent(redirectUrl)}`);
  }

  return {
    tokens: { id_token: event.locals.id_token, access_token: event.locals.access_token },
    environment: event.locals.environment,
    featureFlags: event.locals.featureFlags
  };
};
