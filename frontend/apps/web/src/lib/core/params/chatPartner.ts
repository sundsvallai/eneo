import type { ParamMatcher } from "@sveltejs/kit";

export const match = ((param: string): param is "assistants" | "default" | "group-chats" => {
  return param === "assistants" || param === "default" || param === "group-chats";
}) satisfies ParamMatcher;
