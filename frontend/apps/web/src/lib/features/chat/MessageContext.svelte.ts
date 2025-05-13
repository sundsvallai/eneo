import { createContext } from "$lib/core/context";
import type { ConversationMessage } from "@intric/intric-js";

export const [getMessageContext, setMessageContext] = createContext<{
  current: () => ConversationMessage;
  isLoading: () => boolean;
  isLast: () => boolean;
}>("messageContext");
