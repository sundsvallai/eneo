import typography from "@tailwindcss/typography";
import tailwindConfig from "@intric/ui/styles/tailwind-config";

/** @type {import('tailwindcss').Config} */
export default {
  ...tailwindConfig,
  content: ["./src/**/*.{html,js,svelte,ts}", "../../packages/ui/dist/**/*.svelte"],
  plugins: [typography]
};
