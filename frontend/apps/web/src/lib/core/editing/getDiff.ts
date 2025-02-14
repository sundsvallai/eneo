export type CompareOptions<T> = {
  [key in keyof T]?: T[key] extends Record<string, unknown>
    ? (keyof T[key])[] | true
    : T[key] extends Record<string, unknown>[]
      ? (keyof T[key][number])[] | true
      : true;
};

export type Diff<T extends Record<string, unknown>, Compare extends CompareOptions<T>> = {
  [key in keyof Compare]?: key extends keyof T
    ? Compare[key] extends string[]
      ? T[key] extends Array<Record<string, unknown>>
        ? {
            [field in Compare[key][number]]: T[key][number] extends { [x in field]: unknown }
              ? T[key][number][field]
              : never;
          }[]
        : {
            [field in Compare[key][number]]: T[key] extends { [x in field]: unknown }
              ? T[key][field]
              : never;
          }
      : T[key]
    : never;
};

/**
 * Compare the selected fields and keys of two objects.
 * Will return an object with the calculated diff that can be used in a patch operation.
 * */
export function getDiff<
  T extends Record<string, unknown>,
  K extends T,
  Compare extends CompareOptions<K>
>(
  original: T,
  copy: K,
  options: {
    compare: Compare;
  }
): Diff<K, Compare> {
  const result: Record<string, unknown> = {};

  if (!options?.compare) {
    // Potentially we could implement a full diff here, but for now we just do nothing
    return {};
  }

  // Walk through compairisons
  for (const [key, fields] of Object.entries(options.compare)) {
    // Simple case, compare value directly if primitive
    if (isPrimitive(original[key])) {
      if (copy[key] !== original[key]) result[key] = copy[key];
      continue;
    }

    // If the whole object should be compared, this works for simple arrays and objects
    if (fields === true) {
      const a = JSON.stringify(original[key]);
      const b = JSON.stringify(copy[key]);
      if (a !== b) result[key] = JSON.parse(b);
      continue;
    }

    // Assumptions:
    // - fields is a list of actual fields we should compare
    // - original[key] is an object that has the properties specified in fields
    if (isRecord(original[key]) && isRecord(copy[key])) {
      const a = JSON.stringify(extractFields(original[key], fields));
      const b = JSON.stringify(extractFields(copy[key], fields));
      if (a !== b) result[key] = JSON.parse(b);
    }

    if (isArray(original[key]) && isArray(copy[key])) {
      const a = JSON.stringify(original[key].map((item) => extractFields(item, fields)));
      const b = JSON.stringify(copy[key].map((item) => extractFields(item, fields)));
      if (a !== b) result[key] = JSON.parse(b);
    }
  }

  return result as Diff<K, Compare>;
}

function isPrimitive(value: unknown): value is string | number | boolean {
  return typeof value === "boolean" || typeof value === "string" || typeof value === "number";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isArray(value: unknown): value is Record<string, unknown>[] {
  return value !== null && Array.isArray(value);
}

function extractFields<T extends Record<string, unknown>>(obj: T, fields: (keyof T)[]) {
  return Object.fromEntries(fields.map((field) => [field, obj[field]]));
}
