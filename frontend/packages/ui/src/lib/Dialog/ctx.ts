import { createDialog as createMeltDialog } from "@melt-ui/svelte";
import { getContext, setContext } from "svelte";

const ctxKey = "dialog_" + crypto.randomUUID();

export function createDialog(isAlert: boolean, portal: string | null | undefined) {
  const ctx = createMeltDialog({
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
