import adapter_vercel from "@sveltejs/adapter-vercel";
import adapter_node from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors
  preprocess: vitePreprocess(),
  kit: {
    // Default build will generate a node version of the frontend
    // Set the ADAPTER environment variable to `vercel` for vercel build
    adapter: process.env.ADAPTER === "vercel" ? adapter_vercel() : adapter_node(),
    csp: {
      directives: {
        "script-src": ["self"],
        "script-src-elem": ["self"],
        "script-src-attr": ["self"]
      }
    }
  }
};

export default config;
