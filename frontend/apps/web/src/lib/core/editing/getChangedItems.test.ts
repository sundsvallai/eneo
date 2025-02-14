import { expect, test } from "vitest";
import { getAddedItems, getRemovedItems } from "./getChangedItems";

test("Detect single added item", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "2" }, { id: "3" }, { id: "4" }];

  expect(getAddedItems(a, b)).toEqual([{ id: "4" }]);
});

test("Detect multiple added items", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "2" }, { id: "3" }, { id: "4" }, { id: "5" }];

  expect(getAddedItems(a, b)).toEqual([{ id: "4" }, { id: "5" }]);
});

test("Ignore duplicated added items", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "2" }, { id: "3" }, { id: "4" }, { id: "4" }];

  expect(getAddedItems(a, b)).toEqual([{ id: "4" }]);
});

test("Ignore added duplicated items that already existed", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "2" }, { id: "3" }, { id: "3" }, { id: "5" }];

  expect(getAddedItems(a, b)).toEqual([{ id: "5" }]);
});

test("Ignore removed items when getting added items", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "4" }];

  expect(getAddedItems(a, b)).toEqual([{ id: "4" }]);
});

test("Detect single removed item", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "2" }];

  expect(getRemovedItems(a, b)).toEqual([{ id: "3" }]);
});

test("Detect multiple removed items", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }];

  expect(getRemovedItems(a, b)).toEqual([{ id: "2" }, { id: "3" }]);
});

test("Ignore duplicated removed items", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "2" }];

  expect(getRemovedItems(a, b)).toEqual([{ id: "3" }]);
});

test("Ignore duplicated items that already existed", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "2" }];

  expect(getRemovedItems(a, b)).toEqual([{ id: "3" }]);
});

test("Ignore added items when getting removed items", () => {
  const a = [{ id: "1" }, { id: "2" }, { id: "3" }];
  const b = [{ id: "1" }, { id: "2" }, { id: "4" }];

  expect(getRemovedItems(a, b)).toEqual([{ id: "3" }]);
});
