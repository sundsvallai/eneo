import { createTabs } from "@melt-ui/svelte";
import { getContext, setContext } from "svelte";
import { writable, type Writable } from "svelte/store";

const ctxKey = "content";

export function createContentTabs(initialTab: string | undefined = undefined) {
  const scrolled = writable(0);
  const ctx = createTabs({
    autoSet: true,
    loop: true,
    orientation: "horizontal",
    activateOnFocus: false,
    defaultValue: initialTab
  }) as ReturnType<typeof createTabs> & { states: { scrolled: Writable<number> } };

  ctx.states.scrolled = scrolled;
  setContext<typeof ctx>(ctxKey, ctx);
  return ctx;
}

export function getContentTabs() {
  return getContext<ReturnType<typeof createContentTabs>>(ctxKey);
}

export type ValueState = ReturnType<typeof createContentTabs>["states"]["value"];
