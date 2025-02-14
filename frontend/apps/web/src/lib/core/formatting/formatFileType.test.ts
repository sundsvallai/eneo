import { expect, test } from "vitest";
import { formatFileType } from "./formatFileType";

test("Apply default to null property", () => {
  expect(formatFileType("audio/mp3")).toEqual("MP3");
});

test("Apply default to null property", () => {
  expect(formatFileType("audio/aac")).toEqual("AAC");
});

test("Apply default to null property", () => {
  expect(
    formatFileType("application/vnd.openxmlformats-officedocument.wordprocessingml.document")
  ).toEqual("DOCUMENT");
});
