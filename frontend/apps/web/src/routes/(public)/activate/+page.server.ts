import { DEFAULT_LANDING_PAGE } from "$lib/core/constants.js";
import { env } from "$env/dynamic/private";
import { redirect } from "@sveltejs/kit";

export const load = async (event) => {
  const accessToken = event.cookies.get("acc");

  // If user is not even logged in (=no token found), we redirect to login page instead
  if (!accessToken) {
    redirect(302, "/login");
  }

  const response = await fetch(env.INTRIC_BACKEND_URL + "/api/v1/users/provision/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      zitadel_token: accessToken
    })
  });

  // If the user was created we receive a 200 range code, so we can redirect to the app
  if (response.ok) {
    redirect(302, DEFAULT_LANDING_PAGE);
  }

  // User is logged in to zitadel, but no intric account -> show the activate page
  return {};
};
