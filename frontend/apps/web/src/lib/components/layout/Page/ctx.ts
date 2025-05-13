import { createTabs } from "@melt-ui/svelte";
import { getContext, setContext } from "svelte";
import type { Writable } from "svelte/store";

const ctxKey = "content";

export function createContentTabs(
  initialTab: string | undefined = undefined,
  value: Writable<string> | undefined = undefined,
  onValueChange: ((args: { curr: string; next: string }) => string) | undefined = undefined
) {
  const ctx = createTabs({
    autoSet: true,
    loop: true,
    orientation: "horizontal",
    activateOnFocus: false,
    defaultValue: initialTab,
    value,
    onValueChange
  }) as ReturnType<typeof createTabs>;

  setContext<typeof ctx>(ctxKey, ctx);
  return ctx;
}

export function getContentTabs() {
  return getContext<ReturnType<typeof createContentTabs>>(ctxKey);
}

export type ValueState = ReturnType<typeof createContentTabs>["states"]["value"];
