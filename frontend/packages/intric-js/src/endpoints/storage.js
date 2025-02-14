/** @typedef {import('../client/client').IntricError} IntricError */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initStorage(client) {
  return {
    /**
     * List storage status and settings for current tenant
     * @throws {IntricError}
     * */
    getStats: async () => {
      const res = await client.fetch("/api/v1/storage/", { method: "get" });
      return res;
    },

    /**
     * List all non-personal spaces of this tenant and their corresponding sizes
     *
     * @throws {IntricError}
     */
    listSpaces: async () => {
      const res = await client.fetch("/api/v1/storage/spaces/", {
        method: "get"
      });
      return res.items;
    }
  };
}
