/** @typedef {import('../client/client').IntricError} IntricError */
/** @typedef {import('../types/resources').User} User */
/** @typedef {import('../types/resources').UserSparse} UserSparse */
/** @typedef {import('../types/resources').Tenant} Tenant */

/**
 * @param {import('../client/client').Client} client Provide a client with which to call the endpoints
 */
export function initUser(client) {
  return {
    /**
     * Get info about the currently logged in user.
     * @returns {Promise<import('../types/schema').components["schemas"]["UserPublic"]>}
     * @throws {IntricError}
     * */
    me: async () => {
      const res = await client.fetch("/api/v1/users/me/", { method: "get" });
      return res;
    },

    /**
     * Get info about the currently logged in user's tenant.
     * @returns {Promise<Tenant>}
     * @throws {IntricError}
     * */
    tenant: async () => {
      const res = await client.fetch("/api/v1/users/tenant/", { method: "get" });
      return res;
    },

    /**
     * Generate a new api-key for the currently logged in user.
     * WARNING: Will delete any old api-key!
     * @returns {Promise<{truncated_key: string; key: string;}>}
     * @throws {IntricError}
     * */
    generateApiKey: async () => {
      const res = await client.fetch("/api/v1/users/api-keys/", { method: "get" });
      return res;
    },

    /**
     * Lists all users on this tenant.
     * @overload `{includeDetails: true}` requires super user privileges.
     * @param {{includeDetails: true}} params
     * @return {Promise<User[]>}
     *
     * @overload
     * @param {{includeDetails: false}} [params]
     * @return {Promise<UserSparse[]>}
     *
     * @param {{includeDetails: boolean}} [params]
     * @throws {IntricError}
     * */
    list: async (params) => {
      if (params && params.includeDetails) {
        const res = await client.fetch("/api/v1/admin/users/", { method: "get" });
        return res.items;
      }

      const res = await client.fetch("/api/v1/users/", { method: "get" });
      return res.items;
    },

    /**
     * Registers a new user for the current tenant. Requires super user privileges.
     * @param {Omit<User, "used_tokens" | "email_verified" | "is_superuser" | "quota_limit" | "created_with"> & {password:string}} user
     * @returns {Promise<User>} Returns the created user
     * @throws {IntricError}
     * */
    create: async (user) => {
      const res = await client.fetch("/api/v1/admin/users/", {
        method: "post",
        requestBody: {
          "application/json": user
        }
      });
      return res;
    },

    /**
     * Delete an user by username. Requires super user privileges.
     * @param {{username: string} | User} user User to delete
     * @returns {Promise<boolean>} Returns true on success
     * @throws {IntricError}
     * */
    delete: async (user) => {
      const { username } = user;
      const res = await client.fetch("/api/v1/admin/users/{username}", {
        method: "delete",
        params: { path: { username } }
      });
      return res.success;
    },

    /**
     * Update an existing user. Requires super user privileges.
     * @param {Object} params
     * @param {{username: string} | User} params.user User to update; most important to set the current user name here, as it identifies the user on the server
     * @param {Partial<User> & {password?: string;}} params.update Supply properties to update.
     * @returns {Promise<User>} Returns true on success
     * @throws {IntricError}
     * */
    update: async ({ user, update }) => {
      const { username } = user;

      const res = await client.fetch("/api/v1/admin/users/{username}/", {
        method: "post",
        params: { path: { username } },
        requestBody: { "application/json": update }
      });
      return res;
    }
  };
}
