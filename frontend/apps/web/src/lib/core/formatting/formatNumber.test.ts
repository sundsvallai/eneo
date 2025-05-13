import { expect, test } from "vitest";
import { formatNumber } from "./formatNumber";

// Tests for edge cases (both formats)
test("Format 0", () => {
  expect(formatNumber(0)).toEqual("0");
  expect(formatNumber(0, "compact")).toEqual("0");
});

test("Format NaN", () => {
  expect(formatNumber(NaN)).toEqual("0");
  expect(formatNumber(NaN, "compact")).toEqual("0");
});

// Tests for full format (default)
test("Format negative number with full format", () => {
  expect(formatNumber(-1000)).toEqual("-1,000");
  expect(formatNumber(-1000000)).toEqual("-1,000,000");
});

test("Format small numbers with full format (no commas)", () => {
  expect(formatNumber(1)).toEqual("1");
  expect(formatNumber(999)).toEqual("999");
});

test("Format thousands with full format", () => {
  expect(formatNumber(1000)).toEqual("1,000");
  expect(formatNumber(10000)).toEqual("10,000");
  expect(formatNumber(100000)).toEqual("100,000");
});

test("Format millions with full format", () => {
  expect(formatNumber(1000000)).toEqual("1,000,000");
  expect(formatNumber(10000000)).toEqual("10,000,000");
  expect(formatNumber(100000000)).toEqual("100,000,000");
});

test("Format billions with full format", () => {
  expect(formatNumber(1000000000)).toEqual("1,000,000,000");
});

test("Format with decimals in full format", () => {
  expect(formatNumber(1234.56)).toEqual("1,234.56");
});

// Tests for compact format
test("Format negative number with compact format", () => {
  expect(formatNumber(-1000, "compact")).toEqual("-1K");
});

test("Format small numbers with compact format (no suffix)", () => {
  expect(formatNumber(1, "compact")).toEqual("1");
  expect(formatNumber(999, "compact")).toEqual("999");
});

test("Format thousands with compact format (K)", () => {
  expect(formatNumber(1000, "compact")).toEqual("1K");
  expect(formatNumber(1500, "compact")).toEqual("2K");
  expect(formatNumber(124000, "compact")).toEqual("124K");
});

test("Format millions with compact format (M)", () => {
  expect(formatNumber(1000000, "compact")).toEqual("1M");
  expect(formatNumber(1500000, "compact")).toEqual("2M");
});

test("Format billions with compact format (B)", () => {
  expect(formatNumber(1000000000, "compact")).toEqual("1B");
});

test("Format trillions with compact format (T)", () => {
  expect(formatNumber(1000000000000, "compact")).toEqual("1T");
});

test("Format with decimals in compact format", () => {
  expect(formatNumber(1500, "compact", 1)).toEqual("1.5K");
  expect(formatNumber(1500000, "compact", 2)).toEqual("1.50M");
});
