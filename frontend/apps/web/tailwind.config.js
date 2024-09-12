import defaultTheme from "tailwindcss/defaultTheme";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,svelte,ts}", "../../packages/ui/dist/**/*.svelte"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", ...defaultTheme.fontFamily.sans]
      },

      animation: {
        spin: "spin 3s linear infinite"
      }
    }
  },
  plugins: [require("@tailwindcss/typography")]
};
