import { marked, type TokenizerAndRendererExtension } from "marked";

export { default as Markdown } from "./Markdown.svelte";
export { type CustomRenderers as MarkdownCustomRenderingOptions } from "./CustomComponents";

export function intricMarkdownLexer() {
  const intricInrefRule = /^<inref\s+id="([^"]+)"(?:\s*\/?>|\s*><\/inref>)/;

  const intricInref: TokenizerAndRendererExtension = {
    name: "intricInref",
    level: "inline",
    start(src: string) {
      const idx = src.indexOf("<inref");
      return idx;
    },
    tokenizer(src: string) {
      const match = src.match(intricInrefRule);

      if (match) {
        const id = match[1];

        return {
          type: "intricInref",
          raw: match[0],
          id
        };
      }
    }
  };

  marked.use({ extensions: [intricInref] });
  return {
    lex(source: string) {
      const tokens = marked.lexer(source);
      return tokens;
    }
  };
}
