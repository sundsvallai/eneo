import { getContext, setContext } from "svelte";

export function createContext<T>(description?: string): [get: () => T, set: (value: T) => void] {
  const key = Symbol(description);
  return [
    () => {
      return getContext(key);
    },
    (value: T) => {
      setContext(key, value);
    }
  ];
}
