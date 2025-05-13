import type { Assistant, GroupChat } from "@intric/intric-js";

const validTypes: (GroupChat["type"] | Assistant["type"])[] = [
  "assistant",
  "default-assistant",
  "group-chat"
] as const;
export type ValidChatPartnerType = (typeof validTypes)[number];

export function isValidChatPartnerType(type: string): type is ValidChatPartnerType {
  // We cast, otherwise TS will complain about type not being compatible
  return (validTypes as string[]).includes(type);
}
