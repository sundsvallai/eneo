/* 
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

import { dev } from "$app/environment";
import { env } from "$env/dynamic/private";
import type { Cookies } from "@sveltejs/kit";
import { setFrontendAuthCookie } from "./auth.server";

const MobilityguardCookie = "mobilityguard-verifier" as const;

export async function getMobilityguardLink(redirectBaseUri: string, cookies: Cookies) {
  const authEndpoint = env.MOBILITY_GUARD_AUTH;

  const redirectUri = `${redirectBaseUri}/login/callback`;
  const state = "mobilityguard";
  const scope = "openid%20email";
  const { codeVerifier, codeChallenge } = await createCodePair();

  cookies.set(MobilityguardCookie, codeVerifier, {
    path: "/",
    httpOnly: true,
    // Expires in one hour: 1 * (hour)
    expires: new Date(Date.now() + 1 * (60 * 60 * 1000)),
    secure: dev ? false : true,
    sameSite: "lax"
  });

  const link =
    `${authEndpoint}?scope=${scope}&client_id=intric&response_type=code` +
    `&redirect_uri=${redirectUri}` +
    `&state=${state}` +
    `&code_challenge=${codeChallenge}&code_challenge_method=S256`;

  return link;
}

export async function loginWithMobilityguard(
  redirectBaseUri: string,
  code: string,
  cookies: Cookies
): Promise<boolean> {
  const code_verifier = cookies.get(MobilityguardCookie);

  if (!code_verifier) {
    return false;
  }

  const body = JSON.stringify({
    code,
    code_verifier,
    scope: "openid%20email",
    redirect_uri: `${redirectBaseUri}/login/callback`
  });

  const response = await fetch(
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

  cookies.delete(MobilityguardCookie, { path: "/" });

  const { access_token } = await response.json();
  setFrontendAuthCookie(access_token, cookies);

  return true;
}

// We can't use regualar base64, as it includes the + and / characters.
// We replace them in this implementation. We also remove the added = padding in the end.
// https://datatracker.ietf.org/doc/html/rfc7636#page-8
function base64Encode(data: Uint8Array) {
  return btoa(String.fromCharCode(...data))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=/g, "");
}

function generateCodeVerifier() {
  const data = new Uint8Array(32);
  crypto.getRandomValues(data);
  const verifier = base64Encode(data);

  return verifier;
}

async function generateCodeChallenge(verifier: string) {
  const data = new TextEncoder().encode(verifier);
  const hashed = new Uint8Array(await crypto.subtle.digest("SHA-256", data));
  const challenge = base64Encode(hashed);

  return challenge;
}

async function createCodePair() {
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);
  return { codeVerifier, codeChallenge };
}
