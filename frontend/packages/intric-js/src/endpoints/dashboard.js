/** @typedef {import('../client/client').IntricError} IntricError */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 * @throws {IntricError}
 */
export function initDashboard(client) {
  return {
    /**
     * List all assistants on the users Dashboard
     * @returns {Promise<import('../types/resources').Dashboard>}
     * @throws {IntricError}
     * */
    list: async () => {
      const res = await client.fetch("/api/v1/dashboard/", {
        method: "get"
      });
      return res;
    }
  };
}
