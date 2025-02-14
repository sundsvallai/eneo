export const LoginErrorCode = {
  NO_VERIFIER: "No code verifier found. Please check if cookies are enabled in your browser.",
  NO_TOKEN: "Couldn't get token response from instance.",
  DECODE_ERROR: "Failed to decode response.",
  NO_CONFIG: "No config found in environment."
} as const;

export const providers = ["zitadel"] as const;

export class LoginError extends Error {
  code: keyof typeof LoginErrorCode;
  provider: (typeof providers)[number];
  constructor(
    provider: (typeof providers)[number],
    code: keyof typeof LoginErrorCode,
    message: string = ""
  ) {
    super(LoginErrorCode[code] + message);
    this.name = "LoginError";
    this.provider = provider;
    this.code = code;
  }

  getErrorShortCode() {
    return `${this.provider}_${this.code}`.toLowerCase();
  }

  static getMessageFromShortCode(code: string) {
    const splitIdx = code.indexOf("_");
    const provider = code.substring(0, 1).toUpperCase() + code.substring(1, splitIdx);
    const id = code.substring(splitIdx + 1).toUpperCase() as keyof typeof LoginErrorCode;
    return `${provider}: ${LoginErrorCode[id]}`;
  }
}
