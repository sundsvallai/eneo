import adapter_vercel from "@sveltejs/adapter-vercel";
import adapter_cloudflare from "@sveltejs/adapter-cloudflare";
import adapter_node from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

function getAdapter() {
  if (process.env.ADAPTER === "vercel") {
    return adapter_vercel();
  }
  if (process.env.ADAPTER === "cloudflare") {
    return adapter_cloudflare();
  }
  return adapter_node();
}

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors
  preprocess: vitePreprocess(),
  kit: {
    // Default build will generate a node version of the frontend
    // Set the ADAPTER environment variable to `vercel` for vercel build
    adapter: getAdapter(),
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
