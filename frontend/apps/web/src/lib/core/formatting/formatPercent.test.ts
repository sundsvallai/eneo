import { expect, test } from "vitest";
import { formatPercent } from "./formatPercent";

test("Format 0 percent", () => {
  expect(formatPercent(0)).toEqual("0.00%");
});

test("Format 1 (100%)", () => {
  expect(formatPercent(1)).toEqual("100.00%");
});

test("Format 0.5 (50%)", () => {
  expect(formatPercent(0.5)).toEqual("50.00%");
});

test("Format with different decimal places", () => {
  expect(formatPercent(0.5, 0)).toEqual("50%");
  expect(formatPercent(0.333, 1)).toEqual("33.3%");
  expect(formatPercent(0.333, 3)).toEqual("33.300%");
});

test("Throws error with negative decimal places", () => {
  expect(() => formatPercent(0.5, -1)).toThrow("decimals must be >= 0");
});

test("Format with custom base", () => {
  expect(formatPercent(50, 0, 100)).toEqual("50%");
  expect(formatPercent(250, 0, 1000)).toEqual("25%");
});

test("Format negative percent", () => {
  expect(formatPercent(-0.5)).toEqual("-50.00%");
});

test("Format NaN input", () => {
  expect(formatPercent(NaN)).toEqual("0.00%");
});
