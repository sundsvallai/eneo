import { env } from "$env/dynamic/private";

function getFlagValue(flag: unknown, defaultValue: boolean) {
  if (flag !== undefined && flag !== null) {
    if (typeof flag === "string") {
      return flag.toLowerCase() !== "false";
    }
    if (typeof flag === "boolean") {
      return flag;
    }
    if (typeof flag === "number") {
      return !!flag;
    }
  }
  return defaultValue;
}

export function getFeatureFlags() {
  return Object.freeze({
    newAuth: false,
    /** Should be enabled by default */
    showTemplates: getFlagValue(env.SHOW_TEMPLATES, true),
    showWidgets: false
  });
}
