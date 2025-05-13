/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

/**
 * Login via a combination of MobilityGuard and intric's own endpoints.
 */

import { dev } from "$app/environment";
import { env } from "$env/dynamic/private";
import type { Cookies } from "@sveltejs/kit";
import { createCodePair, encodeState, setFrontendAuthCookie } from "./auth.server";
import { getRequestEvent } from "$app/server";

const MobilityguardCookie = "mobilityguard-verifier" as const;
const scopes = ["openid", "email"];

export async function getMobilityguardLink(event: { url: URL; cookies: Cookies }) {
  const { codeVerifier, codeChallenge } = await createCodePair();

  event.cookies.set(MobilityguardCookie, codeVerifier, {
    path: "/",
    httpOnly: true,
    // Expires in one hour: 1 * (hour)
    expires: new Date(Date.now() + 1 * (60 * 60 * 1000)),
    secure: dev ? false : true,
    sameSite: "lax"
  });

  const searchParams = new URLSearchParams({
    scope: scopes.join(" "),
    client_id: "intric",
    response_type: "code",
    redirect_uri: `${event.url.origin}/login/callback`,
    state: encodeState({
      loginMethod: "mobilityguard",
      next: event.url.searchParams.get("next")
    }),
    code_challenge: codeChallenge,
    code_challenge_method: "S256"
  });

  return env.MOBILITY_GUARD_AUTH + "?" + searchParams.toString();
}

export async function loginWithMobilityguard(code: string): Promise<boolean> {
  const event = getRequestEvent();
  const code_verifier = event.cookies.get(MobilityguardCookie);

  if (!code_verifier) {
    return false;
  }

  const body = JSON.stringify({
    code,
    code_verifier,
    scope: scopes.join("+"),
    redirect_uri: `${event.url.origin}/login/callback`
  });

  const response = await event.fetch(
    `${env.INTRIC_BACKEND_URL}/api/v1/users/login/openid-connect/mobilityguard/`,
    {
      body,
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    }
  );

  if (!response.ok) {
    return false;
  }

  event.cookies.delete(MobilityguardCookie, { path: "/" });

  const data = await response.json();
  const { access_token } = data;
  // Bit weird renaming going on here, but that is how it is, as the backend calls this "access token"
  await setFrontendAuthCookie({ id_token: access_token });

  return true;
}

export function clearMobilityguardCookie(cookies: Cookies) {
  cookies.delete(MobilityguardCookie, { path: "/" });
}
