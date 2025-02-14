import { expect, test } from "vitest";
import { getDiff } from "./getDiff";

test("Detect change in selected prop", () => {
  const a = { id: "1", name: "group1" };
  const b = { id: "1", name: "group2" };

  expect(getDiff(a, b, { compare: { name: true } })).toEqual({ name: "group2" });
});

test("Detect change in child object when comparing all props", () => {
  const a = { id: "1", person: { name: "test", age: 20 } };
  const b = { id: "1", person: { name: "test", age: 30 } };

  expect(getDiff(a, b, { compare: { person: true } })).toEqual({
    person: { name: "test", age: 30 }
  });
});

test("Detect no change in child object when comparing all props", () => {
  const a = { id: "1", person: { name: "test", age: 20 } };
  const b = { id: "1", person: { name: "test", age: 20 } };

  expect(getDiff(a, b, { compare: { person: true } })).toEqual({});
});

test("Detect change in child object when comparing specific prop", () => {
  const a = { id: "1", person: { name: "test", age: 20 } };
  const b = { id: "1", person: { name: "test", age: 30 } };

  expect(getDiff(a, b, { compare: { person: ["age"] } })).toEqual({
    person: { age: 30 }
  });
});

test("Detect change in child object when comparing specific prop, include all specified props", () => {
  const a = { id: "1", person: { name: "test", age: 20 } };
  const b = { id: "1", person: { name: "test", age: 30 } };

  expect(getDiff(a, b, { compare: { person: ["name", "age"] } })).toEqual({
    person: { name: "test", age: 30 }
  });
});

test("Detect combined diff", () => {
  const a = { id: "1", name: "group1", metadata: { title: "link" } };
  const b = { id: "1", name: "group2", metadata: { title: "external" } };
  expect(
    getDiff(a, b, {
      compare: {
        name: true,
        metadata: true
      }
    })
  ).toEqual({ name: "group2", metadata: { title: "external" } });
});

test("Detect array diff", () => {
  const a = { id: "1", groups: [1, 2, 3] };
  const b = { id: "1", groups: [1, 2] };
  expect(getDiff(a, b, { compare: { groups: true } })).toEqual({ groups: [1, 2] });
});

test("Detect deep array diff on full compare", () => {
  const a = {
    id: "1",
    groups: [
      { name: "1", age: 20 },
      { name: "2", age: 20 }
    ]
  };
  const b = {
    id: "1",
    groups: [
      { name: "1", age: 20 },
      { name: "4", age: 30 }
    ]
  };
  expect(getDiff(a, b, { compare: { groups: true } })).toEqual({
    groups: [
      { name: "1", age: 20 },
      { name: "4", age: 30 }
    ]
  });
});

test("Detect deep array diff on specific compare", () => {
  const a = {
    id: "1",
    groups: [
      { name: "1", age: 20 },
      { name: "2", age: 20 }
    ]
  };
  const b = {
    id: "1",
    groups: [
      { name: "1", age: 20 },
      { name: "4", age: 30 }
    ]
  };
  expect(getDiff(a, b, { compare: { groups: ["age"] } })).toEqual({
    groups: [{ age: 20 }, { age: 30 }]
  });
});

test("Detect deep array diff on specific compare, include all compared fields", () => {
  const a = {
    id: "1",
    groups: [
      { name: "1", age: 20 },
      { name: "2", age: 20 }
    ]
  };
  const b = {
    id: "1",
    groups: [
      { name: "1", age: 20 },
      { name: "4", age: 30 }
    ]
  };
  expect(getDiff(a, b, { compare: { groups: ["age", "name"] } })).toEqual({
    groups: [
      { name: "1", age: 20 },
      { name: "4", age: 30 }
    ]
  });
});

test("Detect added prop", () => {
  const a = { id: "1" };
  const b = { id: "1", name: "group2" };
  expect(getDiff(a, b, { compare: { name: true } })).toEqual({ name: "group2" });
});

test("Empty comparison returns empty object", () => {
  const a = { id: "1" };
  const b = { id: "1", name: "group2" };
  expect(getDiff(a, b, { compare: {} })).toEqual({});
});
