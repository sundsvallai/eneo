import type { Assistant } from "@intric/intric-js";

export function isAssistant(item: unknown & { type: string }): item is Assistant {
  return item.type === "assistant";
}
