import { getContext, setContext } from "svelte";
import { type InfoBlob } from "@intric/intric-js";
import { writable } from "svelte/store";
import type { CustomInfoBlobComponent } from "./CustomComponents";

const ctxKey = Symbol("Message references");

export function initReferenceContext(params: {
  references?: InfoBlob[];
  component?: CustomInfoBlobComponent;
}) {
  const data = {
    state: {
      references: writable<InfoBlob[]>(params.references ?? [])
    },
    customComponent: params.component
  };
  setContext(ctxKey, data);
  return data;
}

export function getReferenceContext() {
  return getContext<ReturnType<typeof initReferenceContext>>(ctxKey);
}
