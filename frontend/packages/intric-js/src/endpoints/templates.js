/** @typedef {import('../types/resources').AssistantTemplate} AssistantTemplate */
/** @typedef {import('../types/resources').AppTemplate} AppTemplate */

import { IntricError } from "../client/client";

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initTemplates(client) {
  return {
    /**
     * @overload `{includeDetails: true}` requires super user privileges.
     * @param {{filter: "assistants"}} params
     * @return {Promise<AssistantTemplate[]>}
     *
     * @overload
     * @param {{filter: "apps"}} params
     * @return {Promise<AppTemplate[]>}
     *
     * @overload
     * @param {{filter: never}} [params]
     * @return {Promise<(AssistantTemplate | AppTemplate)[]>}
     *
     * @param {{filter: "assistants" | "apps"}} [params]
     * @returns {Promise<(AssistantTemplate | AppTemplate)[]>}
     * @throws {IntricError}
     * */
    list: async (params) => {
      if (params) {
        if (params.filter === "apps") {
          const res = await client.fetch("/api/v1/templates/apps/", {
            method: "get"
          });
          return res.items;
        } else if (params.filter === "assistants") {
          const res = await client.fetch("/api/v1/templates/assistants/", {
            method: "get"
          });
          return res.items;
        } else {
          throw new IntricError(
            `Template filter option "${params.filter}" does not exist`,
            "CONNECTION",
            0,
            0
          );
        }
      }
      const res = await client.fetch("/api/v1/templates/", {
        method: "get"
      });
      return res.items;
    }
  };
}
