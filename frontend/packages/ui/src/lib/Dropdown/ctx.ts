import { createDropdownMenu } from "@melt-ui/svelte";
import { getContext, setContext } from "svelte";

const ctxKey = "dropdown";

export function createDropdown() {
  const ctx = createDropdownMenu({
    positioning: {
      fitViewport: true,
      flip: true,
      placement: "bottom"
    },
    forceVisible: true,
    loop: true,
    preventScroll: true,
    arrowSize: 12
  });
  setContext<typeof ctx>(ctxKey, ctx);
  return ctx;
}

export function getDropdown() {
  return getContext<ReturnType<typeof createDropdown>>(ctxKey);
}
