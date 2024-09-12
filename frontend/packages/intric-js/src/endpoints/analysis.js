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
     * @param {{ period?: number, includeFollowups?: boolean } | undefined} params.options Get questions of the last x days. Defaults to 30. Include followups defaults to false.
     * @returns {Promise<import('./assistants').AssistantSession["messages"]>}
     * @throws {IntricError}
     * */
    listQuestions: async ({ assistant, options }) => {
      const days_since = options?.period ?? 30;
      const include_followups = options?.includeFollowups ?? false;
      const { id } = assistant;
      const res = await client.fetch("/api/v1/analysis/assistants/{assistant_id}/", {
        method: "get",
        params: {
          path: { assistant_id: id },
          query: { days_since, include_followups }
        }
      });
      return res.items;
    },

    /**
     * Ask an assistant a question. By default the answer is streamed from the backend, you can act on partial answer updates
     * with the onChunk callback. Once the answer has been fully received a complete `Session` object will be returned.
     * @param {Object} params Ask parameters
     * @param  {{id: string} | Assistant} params.assistant Which assistant to ask
     * @param  {{includeFollowups?: boolean, period?: number}} params.options Options for selecting the questions context
     * @param {string} params.question Question to ask
     * @param {(token: string) => void} [params.onAnswer] Callback to run when a new token/word of the answer is received
     * @param {(response: Response) => Promise<void>} [params.onOpen] Callback to run once the initial response of the backend is received
     * @returns {Promise<{answer: string}>} Once the full answer is received it will be returned
     * @throws {IntricError}
     * */
    ask: async ({ assistant, options, question, onAnswer, onOpen }) => {
      const { id: assistant_id } = assistant;
      const { includeFollowups: include_followups, period: days_since } = options;

      let answer = "";

      await client.stream(
        "/api/v1/analysis/assistants/{assistant_id}/",
        {
          params: { path: { assistant_id }, query: { include_followups, days_since } },
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
