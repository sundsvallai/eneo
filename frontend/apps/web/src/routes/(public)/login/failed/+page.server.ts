import { LoginError } from "$lib/features/auth/LoginError.js";

export const load = async (event) => {
  const message = event.url.searchParams.get("message") ?? "Unknown failure. No message received.";
  const errorInfo = event.url.searchParams.get("info");

  return {
    message: errorInfo ? LoginError.getMessageFromShortCode(errorInfo) : "Error: " + message
  };
};
