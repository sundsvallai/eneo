export type Defaults<T> = {
  [key in keyof T]?: T[key] extends number | string | boolean | Array<unknown>
    ? NonNullable<T[key]>
    : Partial<T[key]>;
} & { id?: never };

type ProtectedProperties = "id";

export type AppliedDefaults<
  T extends Record<string, unknown>,
  K extends Record<string, unknown>
> = {
  [key in keyof T]: key extends ProtectedProperties
    ? T[key]
    : key extends keyof K
      ? K[key]
      : T[key];
} & K;

/**
 * Will overwrite the properties of the base object with the supplied defaults if they are not set
 * */
export function applyDefaults<T extends Record<string, unknown>, D extends Defaults<T>>(
  resource: T,
  defaults: D
) {
  for (const key of Object.keys(defaults)) {
    if (resource[key] === undefined || resource[key] === null) {
      //@ts-expect-error `key` might not exist on `resource`, but that is fine
      resource[key] = defaults[key];
    }
  }
  return resource as AppliedDefaults<T, D>;
}
