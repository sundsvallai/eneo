import { dev } from "$app/environment";
import { env } from "$env/dynamic/private";
import jwt, { type JwtPayload } from "jsonwebtoken";
import { type Cookies, type RequestEvent } from "@sveltejs/kit";

export interface TokenData {
  aud?: string | string[];
  exp?: number;
  iat?: number;
  token: string;
}

/**
 * Checks if a valid auth cookie is set, aka the user is logged in
 * - On success: returns the user's token
 * - On failure: returns `null`
 */
export function authenticateUser(event: RequestEvent): TokenData | null {
  const { cookies } = event;
  const userToken = cookies.get("auth") as string;

  if (userToken === undefined) {
    return null;
  }

  let tokenData: TokenData;
  try {
    tokenData = jwt.verify(userToken, env.JWT_SECRET as jwt.Secret) as TokenData;
  } catch (error: unknown) {
    return null;
  }

  return tokenData;
}

/**
 * Try to login an user. If successful, the `auth` cookie will be set and the function returns `true`
 * Otherwise the function will return `false`
 */
export async function loginUser(
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

  const { access_token } = await response.json();
  setFrontendAuthCookie(access_token, cookies);
  return true;
}

export const setFrontendAuthCookie = (access_token: string, cookies: Cookies) => {
  // Decode token to get expiry
  const token_info = jwt.decode(access_token) as JwtPayload;

  /* Regarding expiry:
  1. We first want the frontend token to expire, so we can
  gracefully generate a logout when checking user credentials
  present in cookie.
  2. The cookie expires slightly before the server token;
  if the user is not active on the page they should just
  be prompted with login next time they vist.
  */
  const payload: TokenData = {
    // Expire the frontend token 60 mins prior to server token
    exp: token_info.exp ?? 3600 - 3600,
    iat: Date.now() / 1000,
    aud: token_info.aud,
    token: access_token
  };

  const data = jwt.sign(payload, env.JWT_SECRET as jwt.Secret);

  cookies.set("auth", data, {
    path: "/",
    httpOnly: true,
    // Expires 10 min prior to server token
    expires: new Date((token_info.exp ?? 600 - 600) * 1000),
    secure: dev ? false : true,
    sameSite: "lax"
  });
};

/**
 * Will clear any auth cookie previously set
 * Caveat: The backend will still accept the old token until it expires, there is no denylist
 */
export const logoutUser = (event: RequestEvent) => {
  event.cookies.delete("auth", { path: "/" });
};
