/** @typedef {import('../types/resources').AnalyticsData} AnalyticsData */
/** @typedef {import('../types/resources').Assistant} Assistant */
/** @typedef {import('../client/client').IntricError} IntricError */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initAnalytics(client) {
  return {
    /**
     * Get counts of assistants, sessions and questions.
     * @param {{start?: string, end?: string}} [params] Define start and end date for data; Expects UTC time string.
     * @returns {Promise<AnalyticsData>} The requested data
     * @throws {IntricError}
     * */
    get: async ({ start, end } = { start: undefined, end: undefined }) => {
      const res = await client.fetch("/api/v1/analysis/metadata-statistics/", {
        method: "get",
        params: { query: { start_date: start, end_date: end } }
      });
      return res;
    },

    /**
     * Get total current counts of assistants, sessions and questions.
     * @returns Counts
     * @throws {IntricError}
     * */
    counts: async () => {
      const res = await client.fetch("/api/v1/analysis/counts/", { method: "get" });
      return res;
    },

    /**
     * List all questions of an assistant in a specific period.
     * @param {Object} params
     * @param {{id: string} | Assistant} params.assistant
     * @param {{ start?: string, end?: string, includeFollowups?: boolean } | undefined} params.options Optionally provide start and end date in iso format (YYYY-MM-DD). Include followups defaults to false.
     * @returns {Promise<import('../types/resources').AssistantResponse[]>}
     * @throws {IntricError}
     * */
    listQuestions: async ({ assistant, options }) => {
      const include_followups = options?.includeFollowups ?? false;
      const { id } = assistant;
      const res = await client.fetch("/api/v1/analysis/assistants/{assistant_id}/", {
        method: "get",
        params: {
          path: { assistant_id: id },
          query: {
            from_date: options?.start,
            to_date: options?.end,
            include_followups
          }
        }
      });
      return res.items;
    },

    /**
     * Ask an assistant a question. By default the answer is streamed from the backend, you can act on partial answer updates
     * with the onChunk callback. Once the answer has been fully received a complete `Session` object will be returned.
     * @param {Object} params Ask parameters
     * @param  {{id: string} | Assistant} params.assistant Which assistant to ask
     * @param {{ start?: string, end?: string, includeFollowups?: boolean } | undefined} params.options Optionally provide start and end date in iso format (YYYY-MM-DD). Include followups defaults to false.
     * @param {string} params.question Question to ask
     * @param {(token: string) => void} [params.onAnswer] Callback to run when a new token/word of the answer is received
     * @param {(response: Response) => Promise<void>} [params.onOpen] Callback to run once the initial response of the backend is received
     * @returns {Promise<{answer: string}>} Once the full answer is received it will be returned
     * @throws {IntricError}
     * */
    ask: async ({ assistant, options, question, onAnswer, onOpen }) => {
      const { id: assistant_id } = assistant;

      let answer = "";

      await client.stream(
        "/api/v1/analysis/assistants/{assistant_id}/",
        {
          params: {
            path: { assistant_id },
            query: {
              from_date: options?.start,
              to_date: options?.end,
              include_followups: options?.includeFollowups
            }
          },
          requestBody: { "application/json": { question, stream: true } }
        },
        {
          onOpen: async (response) => {
            if (onOpen) onOpen(response);
          },
          onMessage: (ev) => {
            if (ev.data == "") return;
            try {
              const data = JSON.parse(ev.data);
              if (data.answer) {
                answer += data.answer;
                if (onAnswer) onAnswer(data.answer);
              }
            } catch (e) {
              return;
            }
          }
        }
      );

      return { answer };
    }
  };
}
