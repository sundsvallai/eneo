import { dev } from "$app/environment";
import { IntricError } from "@intric/intric-js";

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
    console.error("client error");
    console.error(error);
  }

  return {
    status,
    message,
    sessionInvalid
  };
};
