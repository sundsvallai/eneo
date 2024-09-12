import { hasPermission } from "$lib/core/hasPermission";
import { writable } from "svelte/store";
import { createContext } from "./context";
import type { CurrentUser, Limits, Tenant } from "@intric/intric-js";

const [getAppContext, setAppContext] = createContext<ReturnType<typeof AppContext>>(
  "Context for app-wide data"
);

function initAppContext(data: AppContextParams) {
  setAppContext(AppContext(data));
}

type AppContextParams = {
  user: CurrentUser;
  tenant: Tenant;
  limits: Limits;
  versions: {
    frontend: string;
    backend: string;
    client: string;
    preview?: { branch?: string; commit?: string };
  };
};

function AppContext(data: AppContextParams) {
  const user = { ...data.user, hasPermission: hasPermission(data.user) };
  const showHeader = writable(true);

  return Object.freeze({
    user,
    tenant: data.tenant,
    limits: data.limits,
    versions: data.versions,
    showHeader
  });
}

export { initAppContext, getAppContext };
