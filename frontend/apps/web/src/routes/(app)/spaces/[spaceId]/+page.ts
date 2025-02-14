/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

import { redirect } from "@sveltejs/kit";

export const load = async (event) => {
  const { currentSpace } = await event.parent();

  if (currentSpace.personal) {
    redirect(302, "/spaces/personal/chat");
  }
  redirect(302, event.url.pathname + "/overview");
};
