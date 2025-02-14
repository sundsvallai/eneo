import { IntricError, type IntricErrorCode } from "@intric/intric-js";
import type { HandleClientError } from "@sveltejs/kit";

export const handleError: HandleClientError = async ({ error, status, message }) => {
  let code: IntricErrorCode = 0;
  if (error instanceof IntricError) {
    status = error.status;
    message = error.getReadableMessage();
    code = error.code;
  } else {
    // On the client we always log the error
    console.error(error);
  }

  return {
    status,
    message,
    code
  };
};
