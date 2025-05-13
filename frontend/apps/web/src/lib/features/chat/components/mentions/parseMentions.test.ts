import { describe, it, expect } from "vitest";
import { parseTokens } from "./parseMentions";

describe("parseMentions", () => {
  describe("parseTokens", () => {
    it("returns an empty array for empty input", () => {
      expect(parseTokens("")).toEqual([]);
    });

    it("returns a single text token for content without mentions", () => {
      const input = "Hello world!";
      const expected = [{ type: "text", content: "Hello world!" }];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("parses a single mention correctly", () => {
      const input = "[[@user]]";
      const expected = [{ type: "mention", handle: "user" }];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("parses text with a mention in the middle", () => {
      const input = "Hello [[@user]]!";
      const expected = [
        { type: "text", content: "Hello " },
        { type: "mention", handle: "user" },
        { type: "text", content: "!" }
      ];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("parses text with a mention at the beginning", () => {
      const input = "[[@user]] says hello";
      const expected = [
        { type: "mention", handle: "user" },
        { type: "text", content: " says hello" }
      ];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("parses text with a mention at the end", () => {
      const input = "Message from [[@user]]";
      const expected = [
        { type: "text", content: "Message from " },
        { type: "mention", handle: "user" }
      ];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("parses multiple mentions correctly", () => {
      const input = "Hello [[@user1]], [[@user2]], and [[@user3]]!";
      const expected = [
        { type: "text", content: "Hello " },
        { type: "mention", handle: "user1" },
        { type: "text", content: ", " },
        { type: "mention", handle: "user2" },
        { type: "text", content: ", and " },
        { type: "mention", handle: "user3" },
        { type: "text", content: "!" }
      ];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("handles consecutive mentions without spaces between them", () => {
      const input = "[[@user1]][[@user2]][[@user3]]";
      const expected = [
        { type: "mention", handle: "user1" },
        { type: "mention", handle: "user2" },
        { type: "mention", handle: "user3" }
      ];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("handles mentions with special characters in handles", () => {
      const input = "Mention [[@user-name_123]]!";
      const expected = [
        { type: "text", content: "Mention " },
        { type: "mention", handle: "user-name_123" },
        { type: "text", content: "!" }
      ];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("ignores invalid mention syntax", () => {
      const input = "This is not a [@user] mention or a [[@user] or a [@user]] one";
      const expected = [
        { type: "text", content: "This is not a [@user] mention or a [[@user] or a [@user]] one" }
      ];
      expect(parseTokens(input)).toEqual(expected);
    });

    it("handles multiline text correctly", () => {
      const input = "Line 1\nMention [[@user]] here\nLine 3";
      const expected = [
        { type: "text", content: "Line 1\nMention " },
        { type: "mention", handle: "user" },
        { type: "text", content: " here\nLine 3" }
      ];
      expect(parseTokens(input)).toEqual(expected);
    });
  });
});
