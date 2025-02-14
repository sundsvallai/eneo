/**
 * Login via intric's own endpoints. This is a legacy login method and requires users
 * to be registered directly in intric with username and password.
 */

import { env } from "$env/dynamic/private";
import type { Cookies } from "@sveltejs/kit";
import { setFrontendAuthCookie } from "./auth.server";

/**
 * Try to login an user. If successful, the `auth` cookie will be set and the function returns `true`
 * Otherwise the function will return `false`
 */
export async function loginWithIntric(
  cookies: Cookies,
  username: string,
  password: string
): Promise<boolean> {
  // Endpoint wants urlencoded data
  const body = new URLSearchParams();
  body.append("username", username);
  body.append("password", password);

  const response = await fetch(`${env.INTRIC_BACKEND_URL}/api/v1/users/login/token/`, {
    body: body,
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
  });

  if (!response.ok) {
    return false;
  }

  try {
    const { access_token } = await response.json();
    // Bit weird renaming going on here, but that is how it is, as the backend calls this "access token"
    await setFrontendAuthCookie({ id_token: access_token }, cookies);
    return true;
  } catch (e) {
    console.error("Failed to decode login response");
    return false;
  }
}
