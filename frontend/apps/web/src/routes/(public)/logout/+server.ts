import { redirect, type RequestEvent } from "@sveltejs/kit";
import { logoutUser } from "$lib/features/auth/auth.server.js";

export const GET = (event: RequestEvent) => {
  logoutUser(event);
  const message = event.url.searchParams.get("message");
  if (message) {
    redirect(302, `/login?message=${message}`);
  }
  redirect(302, "/login?message=logout");
};
