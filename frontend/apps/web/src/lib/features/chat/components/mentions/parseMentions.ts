export type TextToken = {
  type: "text";
  content: string;
};

export type MentionToken = {
  type: "mention";
  handle: string;
};

export type Token = TextToken | MentionToken;

/**
 * Parse a string containing mention syntax ([[@handle]]) into tokens
 *
 * @param text Input text that may contain mention syntax
 * @returns An array of tokens (text segments and mentions)
 *
 * @example
 * // returns [
 * //   { type: "text", content: "Hello " },
 * //   { type: "mention", handle: "user" },
 * //   { type: "text", content: "!" }
 * // ]
 * parseTokens("Hello [[@user]]!")
 */
export function parseTokens(text: string): Token[] {
  const tokens: Token[] = [];
  const mentionRegex = /\[\[@([^\]]+)\]\]/g;

  let lastIndex = 0;
  let match: RegExpExecArray | null;

  // Find all mentions and create tokens
  while ((match = mentionRegex.exec(text)) !== null) {
    // Add text before the mention
    if (match.index > lastIndex) {
      tokens.push({
        type: "text",
        content: text.substring(lastIndex, match.index)
      });
    }

    // Add the mention
    const mentionHandle = match[1];
    tokens.push({
      type: "mention",
      handle: mentionHandle
    });

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text after the last mention
  if (lastIndex < text.length) {
    tokens.push({
      type: "text",
      content: text.substring(lastIndex)
    });
  }

  return tokens;
}
