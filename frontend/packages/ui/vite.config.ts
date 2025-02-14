import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig, type PluginOption } from "vite";
import { intricIcons } from "./src/icons/vite-plugin-intric-icons";

export default defineConfig({
  plugins: [intricIcons(), sveltekit() as PluginOption]
});
