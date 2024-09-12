import { createTabs } from "@melt-ui/svelte";
import { getContext, setContext } from "svelte";

import { writable, type Updater, type Writable } from "svelte/store";

function createSidebarState(initialValue: string | null) {
  const PANEL_CLOSED = "$$_PANEL_CLOSED";
  let value = initialValue ?? PANEL_CLOSED;

  const valueStore = writable(value);
  const panelVisible = writable(false);

  const setValue = (next: string) => {
    value = next;
    valueStore.set(next);
    panelVisible.set(next !== PANEL_CLOSED);
  };

  const set = (next: string) => {
    next = next === value ? PANEL_CLOSED : next;
    const panelVisibilityChanged = next === PANEL_CLOSED || value === PANEL_CLOSED;

    if (document.startViewTransition && panelVisibilityChanged) {
      document.startViewTransition(async () => {
        setValue(next);
      });
      return;
    }

    setValue(next);
  };

  const update = (updater: Updater<string>) => {
    const next = updater(value);
    set(next);
  };

  return {
    subscribe: valueStore.subscribe,
    set,
    update,
    panelVisible
  };
}

const ctxKey = "sidebar";

export function createSidebar(initialValue: string | null = null) {
  // Needs to be typecast as we have added a prop to our custom value store
  const ctx = createTabs({
    autoSet: false,
    orientation: "vertical",
    value: createSidebarState(initialValue),
    activateOnFocus: false
  }) as ReturnType<typeof createTabs> & {
    states: { value: { panelVisible: Writable<boolean> } };
  };

  setContext<typeof ctx>(ctxKey, ctx);
  return ctx;
}

export function getSidebar() {
  return getContext<ReturnType<typeof createSidebar>>(ctxKey);
}
