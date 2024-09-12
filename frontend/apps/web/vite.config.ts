import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig, type PluginOption } from "vite";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";

const file = fileURLToPath(new URL("package.json", import.meta.url));
const json = readFileSync(file, "utf8");
const pkg = JSON.parse(json);

export default defineConfig({
  plugins: [sveltekit() as PluginOption],
  test: {
    include: ["src/**/*.{test,spec}.{js,ts}"]
  },
  server: {
    port: 3000,
    strictPort: true
  },
  define: {
    __FRONTEND_VERSION__: JSON.stringify(pkg.version),
    __VERCEL_ENV__: `"${process.env.VERCEL_ENV}"`,
    __GIT_BRANCH__: `"${process.env.VERCEL_GIT_COMMIT_REF}"`,
    __GIT_COMMIT_SHA__: `"${process.env.VERCEL_GIT_COMMIT_SHA}"`
  }
});
