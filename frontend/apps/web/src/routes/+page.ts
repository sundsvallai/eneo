import { redirect } from "@sveltejs/kit";
import { DEFAULT_LANDING_PAGE } from "$lib/core/constants";

export const load = async () => {
  return redirect(302, DEFAULT_LANDING_PAGE);
};
