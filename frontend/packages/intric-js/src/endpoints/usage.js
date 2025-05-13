/** @typedef {import('../client/client').IntricError} IntricError */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initUsage(client) {
  return {
    tokens: {
      /**
       * List token usage status for current tenant
       * @param {{startDate: string, endDate: string}} [params] Define start and end date for data; Expects UTC time string.
       * @throws {IntricError}
       * */
      getSummary: async (params) => {
        const res = await client.fetch("/api/v1/token-usage/", {
          method: "get",
          params: {
            query: {
              start_date: params?.startDate,
              end_date: params?.endDate
            }
          }
        });
        return res;
      }
    },

    storage: {
      /**
       * List storage status and settings for current tenant
       * @throws {IntricError}
       * */
      getSummary: async () => {
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
    }
  };
}
