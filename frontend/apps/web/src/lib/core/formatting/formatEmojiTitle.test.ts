import { expect, test } from "vitest";
import { formatEmojiTitle } from "./formatEmojiTitle";

test("Remove 🤪", () => {
  expect(formatEmojiTitle("🤪Test")).toEqual("Test");
});

test("Remove 🤪 and space", () => {
  expect(formatEmojiTitle("🤪 Test")).toEqual("Test");
});

test("Do not remove 📚 when at the end", () => {
  expect(formatEmojiTitle("Test 📚")).toEqual("Test 📚");
});

test("Remove 📚", () => {
  expect(formatEmojiTitle("📚Test")).toEqual("Test");
});

test("Remove 📚 and space", () => {
  expect(formatEmojiTitle("📚 Test")).toEqual("Test");
});

test("Do not remove 📚 when at the end", () => {
  expect(formatEmojiTitle("Test 📚")).toEqual("Test 📚");
});

test("Do not remove 📚 when at the end", () => {
  expect(formatEmojiTitle("Test 📚")).toEqual("Test 📚");
});

test("Remove 🇸🇪", () => {
  expect(formatEmojiTitle("🇸🇪Test")).toEqual("Test");
});

test("Remove 🇸🇪 and space", () => {
  expect(formatEmojiTitle("🇸🇪 Test")).toEqual("Test");
});

test("Do not remove 🇸🇪 when at the end", () => {
  expect(formatEmojiTitle("Test 🇸🇪")).toEqual("Test 🇸🇪");
});
