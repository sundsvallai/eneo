import { createSelect as createMeltSelect, type SelectOption } from "@melt-ui/svelte";
import { getContext, setContext } from "svelte";
import type { Writable } from "svelte/store";

const ctxKey = "select";

export function createSelect(
  isMultiSelect: boolean,
  customStore: Writable<SelectOption[] | SelectOption> | undefined,
  fitViewport: boolean,
  disabled?: boolean
) {
  const ctx = createMeltSelect({
    forceVisible: false,
    positioning: {
      placement: "bottom",
      fitViewport,
      sameWidth: true
    },
    portal: null,
    multiple: isMultiSelect,
    selected: customStore,
    disabled
  });
  setContext<typeof ctx>(ctxKey, ctx);
  return ctx;
}

export function getSelect() {
  return getContext<ReturnType<typeof createSelect>>(ctxKey);
}
