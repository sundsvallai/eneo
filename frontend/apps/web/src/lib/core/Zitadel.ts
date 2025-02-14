import type { UserInfo } from "$lib/core/AppContext";

export function createZitadelClient(baseUrl: string, access_token: string, _fetch: typeof fetch) {
  return {
    /** A simple call to check if any idps are configured for this user */
    async getNumOfLinkedIdps() {
      try {
        const userEndpoint = baseUrl + "/auth/v1/users/me/idps/_search";
        const res = await _fetch(userEndpoint, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${access_token}`
          },
          body: JSON.stringify({ limit: 1 })
        });
        const json = await res.json();
        const numberOfIdps = json.details.totalResult ?? 0;
        return numberOfIdps as number;
      } catch (e) {
        console.error("Couldn't get idp info", e);
        return 0;
      }
    },

    async getUserInfo() {
      const userEndpoint = baseUrl + "/auth/v1/users/me/profile";
      const res = await _fetch(userEndpoint, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${access_token}`
        }
      });
      const json = await res.json();
      const userInfo = json.profile;
      if (userInfo === undefined) {
        throw new Error("No profile found!");
      }
      return userInfo as UserInfo;
    },

    async updateUserInfo(update: UserInfo) {
      const userEndpoint = baseUrl + "/auth/v1/users/me/profile";
      const res = await _fetch(userEndpoint, {
        method: "PUT",
        body: JSON.stringify(update),
        headers: {
          Authorization: `Bearer ${access_token}`
        }
      });

      if (res.ok) {
        return true;
      }

      throw new Error(`Status: ${res.status} - Text: ${await res.text()}`);
    }
  };
}
