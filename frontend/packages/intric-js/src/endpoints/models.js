/** @typedef {import('../types/resources').CompletionModel} CompletionModel */
/** @typedef {import('../types/resources').EmbeddingModel} EmbeddingModel */
/** @typedef {import('../client/client').IntricError} IntricError */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initModels(client) {
  return {
    /**
     * List all Models.
     * @returns {Promise<{completionModels: CompletionModel[], embeddingModels: EmbeddingModel[]}>}
     * @throws {IntricError}
     * */
    list: async () => {
      const [completionModelsRes, embeddingModelsRes] = await Promise.allSettled([
        client.fetch("/api/v1/completion-models/", {
          method: "get"
        }),
        client.fetch("/api/v1/embedding-models/", {
          method: "get"
        })
      ]);

      const completionModels =
        completionModelsRes.status === "fulfilled" ? completionModelsRes.value.items : [];
      const embeddingModels =
        embeddingModelsRes.status === "fulfilled" ? embeddingModelsRes.value.items : [];

      return { completionModels, embeddingModels };
    },

    /**
     * Update either an existing Completion Model or Embedding Model, only one can be processed at any time
     * @template {{completionModel: {id:string}, embeddingModel?: never, update:import('../types/fetch').JSONRequestBody<"post", "/api/v1/completion-models/{id}/">} | {completionModel?: never, embeddingModel: {id:string}, update:import('../types/fetch').JSONRequestBody<"post", "/api/v1/embedding-models/{id}/">}} T
     * @param {T} params
     * @returns {Promise<T extends { completionModel: { id: string } } ? CompletionModel : EmbeddingModel>}
     * @throws {IntricError}
     * */
    update: async ({ completionModel, embeddingModel, update }) => {
      if (completionModel) {
        const { id } = completionModel;
        const res = await client.fetch("/api/v1/completion-models/{id}/", {
          method: "post",
          params: { path: { id } },
          requestBody: { "application/json": update }
        });
        /** @ts-expect-error Jsdoc can't properly infer return type */
        return res;
      } else {
        const { id } = embeddingModel;
        const res = await client.fetch("/api/v1/embedding-models/{id}/", {
          method: "post",
          params: { path: { id } },
          requestBody: { "application/json": update }
        });
        /** @ts-expect-error Jsdoc can't properly infer return type */
        return res;
      }
    }
  };
}
