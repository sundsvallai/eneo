import { Marked, marked } from "marked";
import { markedHighlight } from "marked-highlight";
import hljs from "highlight.js/lib/core";
import js from "highlight.js/lib/languages/javascript";
import python from "highlight.js/lib/languages/python";
import c from "highlight.js/lib/languages/c";

// @ts-expect-error : Missing type declarations for insane
import insane from "insane";

hljs.registerLanguage("javascript", js);
hljs.registerLanguage("python", python);
hljs.registerLanguage("c", c);

const insaneConfig = {
  ...insane.defaults,
  allowedAttributes: {
    a: ["href", "name", "target"],
    iframe: ["allowfullscreen", "frameborder", "src"],
    img: ["src"],
    span: ["class"],
    code: ["class"]
  }
};

const markedHljs = new Marked(
  markedHighlight({
    langPrefix: "!bg-transparent hljs language-",
    highlight: (code: string) => {
      return hljs.highlightAuto(code, ["javascript", "python", "c"]).value;
    }
  })
);

export async function parseAndHighlight(source: string) {
  const html = await markedHljs.parse(source, { async: true });
  return insane(html, insaneConfig);
}

export async function parse(source: string) {
  const html = await marked.parse(source, { async: true });
  return insane(html, insaneConfig);
}

export function highlight(source: string) {
  const highlighted = hljs.highlightAuto(source, ["javascript", "python", "c"]).value;
  return insane(highlighted, insaneConfig);
}
