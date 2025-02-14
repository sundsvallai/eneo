import { expect, test } from "vitest";
import { formatWebsiteName } from "./formatWebsiteName";

test("Use website name if it exists", () => {
  expect(formatWebsiteName({ name: "Test", url: "http://test.com/page/route" })).toEqual("Test");
});

test("User shortened URL if no name found", () => {
  expect(formatWebsiteName({ url: "http://test.com/page/route" })).toEqual("test.com/page/route");
});

test("User shortened URL if name set to null", () => {
  expect(formatWebsiteName({ name: null, url: "http://test.com/page/route" })).toEqual(
    "test.com/page/route"
  );
});

test("User shortened URL if name is empty string", () => {
  expect(formatWebsiteName({ name: "", url: "http://test.com/page/route" })).toEqual(
    "test.com/page/route"
  );
});

test("Use full URL if it does not contain //", () => {
  expect(formatWebsiteName({ url: "https:test.com/page/route" })).toEqual(
    "https:test.com/page/route"
  );
});
