import { dev } from "$app/environment";
import { authenticateUser } from "$lib/features/auth/auth.server";
import { IntricError } from "@intric/intric-js";
import { redirect } from "@sveltejs/kit";

function routeRequiresAuth(pathname: string) {
  const publicRoutes = ["/login", "/login/*", "/logout", "/signup", "/embed/*"];

  // Return false if whole route is public
  if (publicRoutes.includes(pathname)) {
    return false;
  }
  // Check if a route pattern matches the pathname
  // Currently only one trailing * is supported
  const wildcardRoutes = publicRoutes.filter((route) => route.endsWith("*"));
  let isProtected = true;
  wildcardRoutes.forEach((route) => {
    if (pathname.startsWith(route.replace("*", ""))) {
      isProtected = false;
    }
  });
  return isProtected;
}

export const handle = async ({ event, resolve }) => {
  const authInfo = authenticateUser(event);

  if (authInfo) {
    event.locals.user = {
      isLoggedIn: true,
      token: authInfo.token
    };
  } else {
    event.locals.user = {
      isLoggedIn: false
    };
    // If not on a public page redirect to login
    if (routeRequiresAuth(event.url.pathname)) {
      const redirectUrl = event.url.pathname + event.url.search;
      redirect(302, `/login?next=${redirectUrl}`);
    }
  }

  return resolve(event);
};

export const handleError = async ({ error, status, message }) => {
  let sessionInvalid = false;

  if (error instanceof IntricError) {
    status = error.status;
    message = error.getReadableMessage(false);
    // We assume the frontend is not generating any real 404 intric errors
    if (error.status === 404 || error.status === 401) {
      sessionInvalid = true;
    }
  }

  if (dev) {
    console.error("server error");
    console.error(error);
  }

  return {
    status,
    message,
    sessionInvalid
  };
};
