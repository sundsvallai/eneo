import { createContext } from "$lib/core/context";
import type { UserIntegration } from "@intric/intric-js";

export const [getAvailableIntegrations, setAvailableIntegrations] =
  createContext<UserIntegration[]>("Integrations context");
