import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vitest/config";
import type { PluginOption } from "vite";
import tailwindcss from "@tailwindcss/vite";
import { paraglideVitePlugin } from "@inlang/paraglide-js";
// Visualiser to analyse bundle sizes
// import { visualizer } from "rollup-plugin-visualizer";

import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { intricIcons } from "@intric/ui/icons/vite-plugin-intric-icons";

const file = fileURLToPath(new URL("package.json", import.meta.url));
const json = readFileSync(file, "utf8");
const pkg = JSON.parse(json);

export default defineConfig({
  plugins: [
    // visualizer({
    //   emitFile: true,
    //   filename: "stats.html"
    // }),
    paraglideVitePlugin({
      project: "./project.inlang",
      outdir: "./src/lib/paraglide",
      strategy: ["url", "cookie", "baseLocale"]
    }) as PluginOption,
    tailwindcss() as PluginOption,
    intricIcons() as PluginOption,
    sveltekit() as PluginOption
  ],
  test: {
    include: ["src/**/*.{test,spec}.{js,ts}"]
  },
  server: {
    host: process.env.HOST ? "0.0.0.0" : undefined,
    port: 3000,
    strictPort: true
  },
  define: {
    __FRONTEND_VERSION__: JSON.stringify(pkg.version),
    __IS_PREVIEW__: process.env.CF_PAGES_BRANCH ? true : process.env.VERCEL_ENV === "preview",
    __GIT_BRANCH__: process.env.CF_PAGES_BRANCH
      ? `"${process.env.CF_PAGES_BRANCH}"`
      : `"${process.env.VERCEL_GIT_COMMIT_REF}"`,
    __GIT_COMMIT_SHA__: process.env.CF_PAGES_COMMIT_SHA
      ? `"${process.env.CF_PAGES_COMMIT_SHA}"`
      : `"${process.env.VERCEL_GIT_COMMIT_SHA}"`
  }
});
