import { assertEquals } from "@std/assert";
import { add } from "./main.ts";

// Test for positive numbers
Deno.test("add positive numbers", () => {
  assertEquals(add(2, 3), 5);
});

// Test for negative numbers
Deno.test("add negative numbers", () => {
  assertEquals(add(-2, -3), -5);
});

// Test for mixed positive and negative numbers
Deno.test("add mixed positive and negative numbers", () => {
  assertEquals(add(5, -3), 2);
});

// Test for adding zero
Deno.test("add zero", () => {
  assertEquals(add(0, 5), 5);
  assertEquals(add(5, 0), 5);
});

// Test for large numbers
Deno.test("add large numbers", () => {
  assertEquals(add(1_000_000, 2_000_000), 3_000_000);
});
