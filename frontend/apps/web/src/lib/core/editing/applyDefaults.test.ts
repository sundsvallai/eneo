import { expect, test } from "vitest";
import { applyDefaults } from "./applyDefaults";

test("Apply default to null property", () => {
  const a: { id: string; name: string | null | undefined } = { id: "1", name: null };
  expect(applyDefaults(a, { name: "test" })).toEqual({ id: "1", name: "test" });
});

test("Apply default to undefined property", () => {
  const a: { id: string; name?: string | null | undefined } = { id: "1" };
  expect(applyDefaults(a, { name: "test" })).toEqual({ id: "1", name: "test" });
});

test("Do not apply default to existing property", () => {
  const a: { id: string; name?: string | null | undefined } = { id: "1", name: "original" };
  expect(applyDefaults(a, { name: "test" })).toEqual({ id: "1", name: "original" });
});

test("Apply multiple defaults", () => {
  const a: {
    id: string;
    name?: string | null | undefined;
    city?: string | null | undefined;
    country?: string | null | undefined;
    currency?: string | null | undefined;
    weather?: string | null | undefined;
  } = {
    id: "1",
    name: "original",
    currency: null,
    weather: null
  };
  expect(applyDefaults(a, { name: "test", city: "Stockholm", currency: "SEK" })).toEqual({
    id: "1",
    name: "original",
    city: "Stockholm",
    currency: "SEK",
    weather: null
  });
});
