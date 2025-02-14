import { browser } from "$app/environment";
import { writable } from "svelte/store";
import { createContext } from "./context";

const [getThemeStore, setThemeStore] = createContext<ReturnType<typeof createThemeStore>>(
  "Store the user selected theme"
);

function initThemeStore() {
  const theme = createThemeStore();
  setThemeStore(theme);
  return theme;
}

export const availableThemes = ["system", "dark", "light"] as const;
export type Theme = (typeof availableThemes)[number];

function createThemeStore() {
  const themeKey = "theme";
  let initial: Theme = "system";

  if (browser) {
    try {
      initial = (window.localStorage.getItem(themeKey) as Theme) ?? "system";
    } catch (e) {
      console.error("No access to localStorage");
    }
  }

  const theme = writable<Theme>(initial);

  return {
    subscribe: theme.subscribe,
    set(newTheme: Theme) {
      if (browser) {
        document.documentElement.dataset.theme = newTheme;
        window.localStorage.setItem(themeKey, newTheme);
      }
      theme.set(newTheme);
    }
  };
}

export { getThemeStore, initThemeStore };
