/** @typedef {import('../client/client').IntricError} IntricError */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initVersion(client) {
  return {
    /**
     * Get backend version.
     * @returns {Promise<string>}
     * @throws {IntricError}
     * */
    get: async () => {
      /** @type {{version: string}}  */
      // @ts-expect-error type for version endpoint not specified in openapi json
      const res = await client.fetch("/version", { method: "get" });
      return res.version;
    }
  };
}
