import { createIntric } from "./src/intric";
export { createIntric } from "./src/intric";
export { createClient, IntricError } from "./src/client/client";
export * from "./src/types/resources";
export type Intric = ReturnType<typeof createIntric>;
