import { DEFAULT_LANDING_PAGE } from "$lib/core/constants";
import { redirect } from "@sveltejs/kit";

export const GET = async () => {
  redirect(302, DEFAULT_LANDING_PAGE);
};
