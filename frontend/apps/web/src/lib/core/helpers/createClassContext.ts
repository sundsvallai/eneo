import { getContext, setContext } from "svelte";

type Constructor<T, Args extends unknown[] = unknown[]> = new (...args: Args) => T;

export function createClassContext<T, Args extends unknown[]>(
  key: string,
  ContextClass: Constructor<T, Args>
) {
  const ctxKey = Symbol(key);

  // Use Args to infer parameters
  function initCtx(...params: Args): T {
    const ctx = new ContextClass(...params);
    setContext(ctxKey, ctx);
    return ctx;
  }

  function getCtx(): T {
    return getContext<T>(ctxKey);
  }

  return [getCtx, initCtx] as const;
}
