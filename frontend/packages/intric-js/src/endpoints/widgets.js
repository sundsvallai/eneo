/** @typedef {import('../types/resources').Widget} Widget */
/** @typedef {import('../client/client').IntricError} IntricError */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initWidgets(client) {
  return {
    /**
     * List widgets, either by assistant or all available ones.
     * @param {{assistant?: {id: string}}} [params] Get widgets of a specific assistant?
     * @returns {Promise<Widget[]>}
     * @throws {IntricError}
     * */
    list: async (params) => {
      const query = params?.assistant?.id ? { assistant_id: params.assistant.id } : undefined;

      const res = await client.fetch("/api/v1/widgets/", {
        method: "get",
        params: {
          query
        }
      });

      return res.items;
    },

    /**
     * Create a new widget.
     * @param {Object} params
     * @param {{id: string} | import('../types/resources').Assistant} params.assistant
     * @param {{name: string; title: string; bot_introduction: string; color: string; size: "small" | "medium" | "large";}} params.settings
     * @returns {Promise<Widget>} The newly created group
     * @throws {IntricError}
     * */
    create: async ({ assistant, settings }) => {
      const res = await client.fetch("/api/v1/widgets/", {
        method: "post",
        requestBody: { "application/json": { ...settings, assistant } }
      });

      return res;
    },

    /**
     * Get info of a widget via its id.
     * @param  {{id: string} | Widget} widget widget
     * @returns {Promise<Widget>} Full info about the queried widget
     * @throws {IntricError}
     * */
    get: async (widget) => {
      const { id } = widget;
      const res = await client.fetch("/api/v1/widgets/{id}/", {
        method: "get",
        params: { path: { id } }
      });
      return res;
    },

    /**
     * Update an existing widget.
     * @param {Object} params
     * @param {{id: string} | Widget} params.widget The widget you want to update
     * @param { Partial<Widget> } params.update - Either provide the updated widget or the parameters to update.
     * @returns {Promise<Widget>} The updated widget
     * */
    update: async ({ widget, update }) => {
      const { id } = widget;
      const res = await client.fetch("/api/v1/widgets/{id}/", {
        method: "post",
        params: { path: { id } },
        requestBody: { "application/json": update }
      });
      return res;
    },

    /**
     * Delete the specified widget.
     * @param {{id: string} | Widget} widget - Either provide the widget to delete or a specified id.
     * @returns {Promise<{success: boolean}>} The result
     * */
    delete: async (widget) => {
      const { id } = widget;
      const res = await client.fetch("/api/v1/widgets/{id}/", {
        method: "delete",
        params: { path: { id } }
      });
      return res;
    },

    privacyPolicy: {
      /**
       * Get the privacy policy URL. Same for all widgets.
       * @returns {Promise<string | null>} Url of the policy or `null` if none set.
       * @throws {IntricError}
       * */
      get: async () => {
        const res = await client.fetch("/api/v1/widgets/settings/privacy-policy/", {
          method: "get"
        });
        return res.url ?? null;
      },

      /**
       * Delete the privacy policy.
       * @returns {Promise<boolean>} `true` if the deletion was successful
       * @throws {IntricError}
       * */
      delete: async () => {
        const res = await client.fetch("/api/v1/widgets/settings/privacy-policy/", {
          method: "post",
          requestBody: { "application/json": { url: null } }
        });
        return res.url === null;
      },

      /**
       * Update the privacy policy.
       * @param {string} url - The new URL for the privacy policy.
       * @returns {Promise<string | null>} Updated privacy policy or null if none set
       * @throws {IntricError}
       */
      update: async (url) => {
        const res = await client.fetch("/api/v1/widgets/settings/privacy-policy/", {
          method: "post",
          requestBody: { "application/json": { url } }
        });
        return res.url ?? null;
      }
    }
  };
}
