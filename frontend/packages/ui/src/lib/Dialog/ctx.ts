import { createDialog as createMeltDialog } from "@melt-ui/svelte";
import { getContext, setContext } from "svelte";
import type { Writable } from "svelte/store";

const ctxKey = Symbol("ui-dialog");

export function createDialog(
  isAlert: boolean,
  portal: string | null | undefined,
  open: Writable<boolean> | undefined
) {
  const ctx = createMeltDialog({
    open,
    portal,
    forceVisible: true,
    closeOnOutsideClick: true,
    escapeBehavior: "defer-otherwise-close",
    role: isAlert ? "alertdialog" : "dialog"
  });
  setContext<typeof ctx>(ctxKey, ctx);
  return ctx;
}

export function getDialog() {
  return getContext<ReturnType<typeof createDialog>>(ctxKey);
}

export type OpenState = ReturnType<typeof createDialog>["states"]["open"];
