function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

/** Basic diffing function to find updates between two objects */
export function getDiff(a: Record<string, unknown>, b: Record<string, unknown>) {
  // Copy so we don't change the actual object b
  const diff: Record<string, unknown> = JSON.parse(JSON.stringify(b));

  // Strategy here is to drop all fields from diff that are the same as "a" and then return diff
  for (const [key, value] of Object.entries(a)) {
    if (Object.hasOwn(diff, key)) {
      // Compare values and drop value from diff object if there is no diff
      if (JSON.stringify(value) === JSON.stringify(diff[key])) {
        diff[key] = undefined;
        delete diff[key];
        continue;
      }

      // Now that we know the respective property has a diff we need to check for two more cases:

      // 1. The updated property is an Array
      // Here we make a deliberate choice to not deep compare the individual array elements. We know there is a change
      // somewhere in the array, but for our use case it is enough (for now) to just return the edited array
      if (Array.isArray(value)) {
        if (Array.isArray(diff[key])) {
          continue;
        }
      }

      // 2. The property is an object
      // For objects we actually want to deep compare them
      if (isRecord(value)) {
        if (isRecord(diff[key])) {
          // Do a recursive get diff on the object
          diff[key] = getDiff(value, diff[key]);
          continue;
        }
      }

      // Fallthrough case
      // The property is a value, in which case we do not need to do anything, as we just keep the new value
      continue;
    }
  }

  return diff;
}

type MakeEditableFn = <T extends Record<string, unknown>>(original: T) => Editable<T>;

type NormalisedProp<T> =
  T extends Array<{ id: unknown }>
    ? { id: T[0]["id"] }[]
    : T extends { id: unknown }
      ? { id: T["id"] }
      : never;

type Normalise<T, Property extends string> = Omit<T, Property> & {
  [P in keyof T & Property]: NormalisedProp<T[P]>;
};

export type Editable<T> = Normalise<T, "groups" | "completion_model" | "embedding_model"> & {
  /**
   * Will return a partial object that only includes the properties that have changed.
   * After that the previous changes will become the new baseline for diffing, so
   * `getEdits()` finalizes the current editing session.
   */
  getEdits: () => Partial<Normalise<T, "groups" | "completion_model" | "embedding_model">>;
  /**
   * Will return the underlying reference against which te diffing runs
   */
  getOriginal: () => Normalise<T, "groups" | "completion_model" | "embedding_model">;
  /**
   * Will update both the current editable values and original reference to the provided value,
   * e.g. when getting an updated version from the server
   */
  updateWithValue: (value: T) => void;
};

// This is a bit of a hack for now; as we sometimes need different data shapes for updating a resource
// vs. the resource we get from the server, namely converting groups etc. to the {id: string} format
function normaliseProp(obj: unknown, prop: string) {
  function reduceToIdProp(obj: unknown) {
    const reduce = (obj: unknown) => {
      if (isRecord(obj) && Object.hasOwn(obj, "id")) {
        return { id: obj.id };
      }
    };
    if (Array.isArray(obj)) {
      return obj.map((item) => reduce(item));
    }
    return reduce(obj);
  }

  if (isRecord(obj) && Object.hasOwn(obj, prop)) {
    obj[prop] = reduceToIdProp(obj[prop]);
  }
}

/**
 * Make an editable copy of a resource with a getEdits() method to only get updated values.
 *
 * Useful when calling update enpoints in the backend, so we only send actual updated values back.
 *
 * HINT: The diffing algorithm used will not deep-compare arrays and just use the new value instead
 * if there was any change somewhere in the array!
 *
 * WARNING: This is a bit memory intensive as the editable object stores two deep copies of the original data
 * structure to operate completely independent from it, so be careful when using this on large objects.
 */
export const makeEditable: MakeEditableFn = (original) => {
  // Deep clone to keep the original unchanged (important for diffing)
  let _reference = JSON.parse(JSON.stringify(original));
  // Remove interfering props (only id is relevant for changing these props)
  normaliseProp(_reference, "groups");
  normaliseProp(_reference, "completion_model");
  normaliseProp(_reference, "embedding_model");
  // Deep clone to not have changes leak into input object on nested properties
  const _editable = JSON.parse(JSON.stringify(_reference));

  _editable.getEdits = function () {
    const diffed = getDiff(_reference, this);
    // Once diff is calculated the current state becomes the new reference
    _reference = JSON.parse(JSON.stringify(this));
    return diffed as Partial<typeof original>;
  };
  _editable.getOriginal = function () {
    return _reference;
  };
  _editable.updateWithValue = function (value: typeof original) {
    normaliseProp(value, "groups");
    normaliseProp(value, "completion_model");
    normaliseProp(value, "embedding_model");
    _reference = JSON.parse(JSON.stringify(value));
    Object.assign(this, value);
  };
  return _editable;
};
