import { expect, test } from "vitest";
import { getDiff, makeEditable } from "./editable";

test("Detect name diff", () => {
  const a = { id: "1", name: "group1" };
  const b = { id: "1", name: "group2" };
  expect(getDiff(a, b)).toEqual({ name: "group2" });
});

test("Detect nested title diff", () => {
  const a = { id: "1", name: "group1", metadata: { title: "link" } };
  const b = { id: "1", name: "group1", metadata: { title: "external" } };
  expect(getDiff(a, b)).toEqual({ metadata: { title: "external" } });
});

test("Detect combined diff", () => {
  const a = { id: "1", name: "group1", metadata: { title: "link" } };
  const b = { id: "1", name: "group2", metadata: { title: "external" } };
  expect(getDiff(a, b)).toEqual({ name: "group2", metadata: { title: "external" } });
});

test("Detect deep diff", () => {
  const a = { id: "1", name: "group1", metadata: { title: "link", draft: { saved: true } } };
  const b = { id: "1", name: "group1", metadata: { title: "link", draft: { saved: false } } };
  expect(getDiff(a, b)).toEqual({ metadata: { draft: { saved: false } } });
});

test("Detect array diff", () => {
  const a = { id: "1", groups: [1, 2, 3] };
  const b = { id: "1", groups: [1, 2] };
  expect(getDiff(a, b)).toEqual({ groups: [1, 2] });
});

test("Detect added prop", () => {
  const a = { id: "1" };
  const b = { id: "1", name: "group2" };
  expect(getDiff(a, b)).toEqual({ name: "group2" });
});

test("Handle null values correctly", () => {
  const a = { id: null, name: "group1" };
  const b = { name: "group2" };
  const c = { name: "group2", empty: null };
  const d = { id: "1" };
  expect(getDiff(a, b)).toEqual({ name: "group2" });
  expect(getDiff(a, c)).toEqual({ name: "group2", empty: null });
  expect(getDiff(a, d)).toEqual({ id: "1" });
});

test("Ignore dropped prop", () => {
  const a = { id: "1", is_public: false };
  const b = { id: "1", name: "group2" };
  expect(getDiff(a, b)).toEqual({ name: "group2" });
});

test("Editable", () => {
  const a = { id: "1", is_public: false };
  const b = makeEditable(a);
  b.is_public = true;
  expect(b.getEdits()).toEqual({ is_public: true });
});

test("Editable deep", () => {
  const a = { id: "1", is_public: false, deep: { title: "test", deeper: { now: "test" } } };
  const b = makeEditable(a);
  b.deep.title = "new";
  b.deep.deeper.now = "next";
  // Reference is kept to original and changing nested props on b did not change them on a
  expect(b.getOriginal()).toEqual(a);
  expect(b.getEdits()).toEqual({ deep: { title: "new", deeper: { now: "next" } } });
});

test("Editable sets new original/base reference after getEdits()", () => {
  const a = { prop: "original" };
  const b = makeEditable(a);
  b.prop = "edited";
  expect(b.getEdits()).toEqual({ prop: "edited" });
  // After a call to getEdits we expect the edited state to become the new ground truth
  expect(b.getOriginal()).toEqual({ prop: "edited" });
});

test("Set external new value", () => {
  const a = { prop: "original" };
  const b = makeEditable(a);
  b.prop = "edited";
  expect(b.getEdits()).toEqual({ prop: "edited" });
  // After a call to getEdits we expect the edited state to become the new ground truth
  b.updateWithValue({ prop: "external" });
  // Should take new value
  expect(b.getOriginal()).toEqual({ prop: "external" });
  // Should show no edits
  expect(b.getEdits()).toEqual({});
  // Gets new edits correct
  b.prop = "edited";
  expect(b.getEdits()).toEqual({ prop: "edited" });
});

test("Group prop is normalised", () => {
  const a = { prop: "original", groups: [{ id: 1, name: "any" }] };
  const b = makeEditable(a);
  b.groups = [...b.groups, { id: 2 }];
  expect(b.getOriginal()).toEqual({ prop: "original", groups: [{ id: 1 }] });
  expect(b.getEdits()).toEqual({ groups: [{ id: 1 }, { id: 2 }] });
});

test("Group and embedding model props are normalised", () => {
  const a = {
    prop: "original",
    groups: [{ id: 1, name: "any" }],
    embedding_model: { id: 1, name: "any" }
  };
  const b = makeEditable(a);
  b.groups = [...b.groups, { id: 2 }];
  expect(b.getOriginal()).toEqual({
    prop: "original",
    groups: [{ id: 1 }],
    embedding_model: { id: 1 }
  });
  expect(b.getEdits()).toEqual({ groups: [{ id: 1 }, { id: 2 }] });
});

test("Normalising does not change original object passed into makeEditable", () => {
  const a = {
    prop: "original",
    groups: [{ id: 1, name: "any" }],
    embedding_model: { id: 1, name: "any" }
  };
  makeEditable(a);
  expect(a).toEqual({
    prop: "original",
    groups: [{ id: 1, name: "any" }],
    embedding_model: { id: 1, name: "any" }
  });
});
