import defaultTheme from "tailwindcss/defaultTheme";
import typography from "@tailwindcss/typography";

/** @type {(variableName: string) => string} */
function color(variableName) {
  return `var(--${variableName})`;
}

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    darkMode: "class",
    extend: {
      backgroundColor: {
        primary: color("background-primary"),
        secondary: color("background-secondary"),
        tertiary: color("background-tertiary"),
        "overlay-stronger": color("background-overlay-stronger"),
        "overlay-default": color("background-overlay-default"),
        "overlay-dimmer": color("background-overlay-dimmer"),
        "hover-stronger": color("background-hover-stronger"),
        "hover-default": color("background-hover-default"),
        "hover-dimmer": color("background-hover-dimmer"),
        "hover-on-fill": color("background-hover-on-fill")
      },
      gradientColorStops: {
        "bg-primary": color("background-primary"),
        "bg-secondary": color("background-secondary"),
        "bg-tertiary": color("background-tertiary")
      },
      textColor: {
        primary: color("text-primary"),
        secondary: color("text-secondary"),
        muted: color("text-muted"),
        "on-fill": color("text-on-fill")
      },
      borderColor: {
        strongest: color("border-strongest"),
        stronger: color("border-stronger"),
        default: color("border-default"),
        dimmer: color("border-dimmer"),
        "on-fill": color("border-on-fill")
      },
      ringColor: {
        strongest: color("border-strongest"),
        stronger: color("border-stronger"),
        default: color("border-default"),
        dimmer: color("border-dimmer")
      },
      colors: {
        brand: {
          intric: color("brand-intric")
        },
        accent: {
          stronger: color("accent-stronger"),
          default: color("accent-default"),
          dimmer: color("accent-dimmer")
        },
        negative: {
          stronger: color("negative-stronger"),
          default: color("negative-default"),
          dimmer: color("negative-dimmer")
        },
        warning: {
          stronger: color("warning-stronger"),
          default: color("warning-default"),
          dimmer: color("warning-dimmer")
        },
        positive: {
          stronger: color("positive-stronger"),
          default: color("positive-default"),
          dimmer: color("positive-dimmer")
        },
        label: {
          stronger: color("label-stronger"),
          default: color("label-default"),
          dimmer: color("label-dimmer")
        },
        dynamic: {
          stronger: color("dynamic-stronger"),
          default: color("dynamic-default"),
          dimmer: color("dynamic-dimmer")
        }
      },
      typography: {
        DEFAULT: {
          css: {
            "--tw-prose-body": "var(--text-primary)",
            "--tw-prose-headings": "var(--text-primary)",
            "--tw-prose-lead": "var(--text-primary)",
            "--tw-prose-links": "var(--text-primary)",
            "--tw-prose-bold": "var(--text-primary)",
            "--tw-prose-counters": "var(--text-muted)",
            "--tw-prose-bullets": "var(--text-muted)",
            "--tw-prose-hr": "var(--text-muted)",
            "--tw-prose-quotes": "var(--text-secondary)",
            "--tw-prose-quote-borders": "var(--accent-stronger)",
            "--tw-prose-captions": "var(--text-primary)",
            "--tw-prose-kbd": "var(--text-primary)",
            "--tw-prose-kbd-shadows": "var(--shadow-default)",
            "--tw-prose-code": "var(--text-primary)",
            "--tw-prose-pre-code": "var(--text-on-fill)",
            "--tw-prose-pre-bg": "var(--background-overlay-stronger)",
            "--tw-prose-th-borders": "var(--border-default)",
            "--tw-prose-td-borders": "var(--border-dimmer)"
          }
        }
      },
      boxShadowColor: {
        DEFAULT: "var(--shadow-default)",
        sm: "var(--shadow-default)",
        md: "var(--shadow-default)",
        lg: "var(--shadow-stronger)",
        xl: "var(--shadow-stronger)"
      },
      fontFamily: {
        sans: ["Inter", ...defaultTheme.fontFamily.sans]
      },
      animation: {
        spin: "spin 3s linear infinite"
      }
    }
  },
  plugins: [typography]
};
