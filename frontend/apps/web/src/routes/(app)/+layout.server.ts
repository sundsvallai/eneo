import { env } from "$env/dynamic/private";
import { redirect } from "@sveltejs/kit";

export const load = async (event) => {
  if (!event.locals.id_token) {
    // This should already have happend in the handle hook
    const redirectUrl = event.url.pathname + event.url.search;
    redirect(302, `/login?next=${encodeURIComponent(redirectUrl)}`);
  }

  return {
    tokens: { id_token: event.locals.id_token, access_token: event.locals.access_token },
    baseUrl: env.INTRIC_BACKEND_URL,
    authUrl: env.ZITADEL_INSTANCE_URL ?? null,
    frontendVersion: __FRONTEND_VERSION__,
    previewEnv: __IS_PREVIEW__ ? { branch: __GIT_BRANCH__, commit: __GIT_COMMIT_SHA__ } : undefined,
    featureFlags: event.locals.featureFlags,
    feedbackFormUrl: env.FEEDBACK_FORM_URL,
    integrationRequestFormUrl: env.REQUEST_INTEGRATION_FORM_URL
  };
};
