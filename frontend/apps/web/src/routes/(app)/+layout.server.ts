import { env } from "$env/dynamic/private";
import { redirect } from "@sveltejs/kit";

export const load = async (event) => {
  if (!event.locals.user.isLoggedIn) {
    // This should already have happend in the handle hook
    const redirectUrl = event.url.pathname + event.url.search;
    redirect(302, `/login?next=${redirectUrl}`);
  }

  return {
    token: event.locals.user.token,
    baseUrl: env.INTRIC_BACKEND_URL,
    frontendVersion: __FRONTEND_VERSION__,
    vercelEnv:
      __VERCEL_ENV__ && __VERCEL_ENV__ === "preview"
        ? { branch: __GIT_BRANCH__, commit: __GIT_COMMIT_SHA__ }
        : undefined
  };
};
