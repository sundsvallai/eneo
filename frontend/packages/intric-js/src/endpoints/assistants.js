/** @typedef {import('../types/resources').Assistant} Assistant */
/** @typedef {import('../types/resources').AssistantSession} AssistantSession */
/** @typedef {import('../types/resources').AssistantResponse} AssistantResponse */
/** @typedef {import('../types/resources').Group} Group */
/** @typedef {import('../client/client').IntricError} IntricError */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initAssistants(client) {
  return {
    /**
     * List all assistants.
     * @param {{includePublic?: boolean, includeTenant?: boolean} | undefined} [options] Include public assistants? Include all assistant's of this tenant (requires superuser)? Both default to `false`
     * @returns {Promise<Assistant[]>}
     * @throws {IntricError}
     * */
    list: async (options) => {
      const include_public = options?.includePublic ?? false;
      const for_tenant = options?.includeTenant ?? false;

      const res = await client.fetch("/api/v1/assistants/", {
        method: "get",
        params: { query: { include_public, for_tenant } }
      });
      return res.items;
    },

    /**
     * Create a new assistant
     * @param {import('../types/fetch').JSONRequestBody<"post", "/api/v1/assistants/"> | {spaceId: string, name: string}} assistant
     * @throws {IntricError}
     * */
    create: async (assistant) => {
      if ("spaceId" in assistant) {
        const { spaceId: id, name } = assistant;
        const res = await client.fetch("/api/v1/spaces/{id}/applications/assistants/", {
          method: "post",
          params: {
            path: {
              id
            }
          },
          requestBody: {
            "application/json": { name }
          }
        });
        return res;
      }

      const res = await client.fetch("/api/v1/assistants/", {
        method: "post",
        requestBody: {
          "application/json": assistant
        }
      });
      return res;
    },

    /**
     * Transfer an assistant into a different space. Needs matching models to be available
     * Will throw error if not possible
     * @param {{assistant: {id: string}, targetSpace: {id: string}, moveResources?: boolean}} params
     * @throws {IntricError}
     * */
    transfer: async ({ assistant, targetSpace, moveResources }) => {
      const { id } = assistant;
      await client.fetch("/api/v1/assistants/{id}/transfer/", {
        method: "post",
        params: { path: { id } },
        requestBody: {
          "application/json": {
            target_space_id: targetSpace.id,
            move_resources: moveResources
          }
        }
      });
      return true;
    },

    /**
     * Get info of an assistant via its id.
     * @param  {{id: string} | Assistant} assistant assistant
     * @returns {Promise<Assistant>} Full info about the queried assistant
     * @throws {IntricError}
     * */
    get: async (assistant) => {
      const { id } = assistant;
      const res = await client.fetch("/api/v1/assistants/{id}/", {
        method: "get",
        params: { path: { id } }
      });
      return res;
    },

    /**
     * Update an existing assistant.
     * @param {Object} params
     * @param {{id: string} | Assistant} params.assistant The assistant you want to update
     * @param {import('../types/fetch').JSONRequestBody<"post", "/api/v1/assistants/{id}/">} params.update - Either provide the updated assistant or the parameters to update.
     * @returns {Promise<Assistant>} The updated assistant
     * */
    update: async ({ assistant, update }) => {
      const { id } = assistant;
      const res = await client.fetch("/api/v1/assistants/{id}/", {
        method: "post",
        params: { path: { id } },
        requestBody: { "application/json": update }
      });
      return res;
    },

    /**
     * Delete a specific assistant.
     * @param  {{id: string} | Assistant} assistant assistant
     * @returns {Promise<Assistant>} The deleted assistant
     * @throws {IntricError}
     * */
    delete: async (assistant) => {
      const { id } = assistant;
      const res = await client.fetch("/api/v1/assistants/{id}/", {
        method: "delete",
        params: { path: { id } }
      });
      return res;
    },

    /**
     * Ask an assistant a question. By default the answer is streamed from the backend, you can act on partial answer updates
     * with the onChunk callback. Once the answer has been fully received a complete `Session` object will be returned.
     * @param {Object} params Ask parameters
     * @param  {{id: string} | Assistant} params.assistant Which assistant to ask
     * @param {{id: string | null} | AssistantSession | undefined} params.session Session Id of a session to continue, `null` to start a new session
     * @param {string} params.question Question to ask
     * @param {{id: string}[] | undefined} params.files Question to ask
     * @param {(token: string) => void} [params.onAnswer] Callback to run when a new token/word of the answer is received
     * @param {(response: Response) => Promise<void>} [params.onOpen] Callback to run once the initial response of the backend is received
     * @returns {Promise<AssistantResponse>} Once the full answer is received it will be returned
     * @throws {IntricError}
     * */
    ask: async ({ assistant, session, question, files, onAnswer, onOpen }) => {
      const { id } = assistant;
      const session_id = session?.id ?? undefined;

      let answer = "";
      /** @type AssistantResponse */
      let response = {};

      const endpoint = session_id
        ? "/api/v1/assistants/{id}/sessions/{session_id}/"
        : "/api/v1/assistants/{id}/sessions/";

      await client.stream(
        endpoint,
        {
          params: { path: { id, session_id } },
          requestBody: { "application/json": { question, files, stream: true } }
        },
        {
          onOpen: async (response) => {
            if (onOpen) onOpen(response);
          },
          onMessage: (ev) => {
            if (ev.data == "") return;
            try {
              const data = JSON.parse(ev.data);
              response = data;
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

      response.question = question;
      response.answer = answer;
      return response;
    },

    /**
     * List all sessions of an assistant.
     * @param {{id: string} | Assistant} assistant
     * @returns {Promise<Omit<AssistantSession, "messages">[]>}
     * @throws {IntricError}
     * */
    listSessions: async (assistant) => {
      const { id } = assistant;
      const res = await client.fetch("/api/v1/assistants/{id}/sessions/", {
        method: "get",
        params: { path: { id } }
      });
      return res.items;
    },

    /**
     * Get a specific session of an assistant. This will also load the message history for this specific session
     * @param {Object} params
     * @param {{id: string}} params.assistant
     * @param {{id: string}} params.session
     * @returns {Promise<AssistantSession>}
     * @throws {IntricError}
     * */
    getSession: async ({ assistant, session }) => {
      const { id } = assistant;
      const { id: session_id } = session;
      const res = await client.fetch("/api/v1/assistants/{id}/sessions/{session_id}/", {
        method: "get",
        params: { path: { id, session_id } }
      });
      return res;
    },

    /**
     * Delete a specific session of an assistant. Returns the deleted session.
     * @param {Object} params
     * @param {{id: string} | Assistant} params.assistant
     * @param {{id: string} | AssistantSession} params.session
     * @returns {Promise<AssistantSession>}
     * @throws {IntricError}
     * */
    deleteSession: async ({ assistant, session }) => {
      const { id } = assistant;
      const { id: session_id } = session;
      const res = await client.fetch("/api/v1/assistants/{id}/sessions/{session_id}/", {
        method: "delete",
        params: { path: { id, session_id } }
      });
      return res;
    }
  };
}
