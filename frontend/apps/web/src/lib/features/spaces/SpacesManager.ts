/* 
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

import { goto } from "$app/navigation";
import { createContext } from "$lib/core/context";
import type { Intric, ResourcePermission, Space, SpaceSparse } from "@intric/intric-js";
import { derived, get, writable, type Readable } from "svelte/store";

const [getSpacesManager, setSpacesManager] = createContext<ReturnType<typeof SpacesManager>>(
  "Manages spaces / projects"
);

/**
 * Initialise the SpacesManger in its context.
 * Retrieve it via `getSpacesManager()`
 */
function initSpacesManager(data: SpacesManagerParams) {
  const manager = SpacesManager(data);
  setSpacesManager(manager);
  return manager;
}

type SpacesManagerParams = {
  /** Initialise with a list of existing spaces */
  spaces: SpaceSparse[];
  /** Provide the initial starting space – personal space if user hasn't requested a different one */
  currentSpace: Space;
  intric: Intric;
};

function SpacesManager(data: SpacesManagerParams) {
  // Setup variables --------------------------------------------------------
  const { intric } = data;

  const userSpaces = writable(data.spaces);
  const currentSpace = writable(data.currentSpace);

  // Function definitions --------------------------------------------------------
  /** Will update the current space if a new space is passed in via page data */
  function watchPageData(data: { currentSpace: Space }) {
    if (data.currentSpace.id !== get(currentSpace).id) {
      currentSpace.set(data.currentSpace);
    }
  }

  /** Updates the internal state of accessible spaces and returns the updated list */
  async function refreshSpaces() {
    try {
      const updated = await intric.spaces.list();
      userSpaces.set(updated);
      return updated;
    } catch (e) {
      console.error("Error updating spaces", e);
    }
  }

  async function refreshCurrentSpace() {
    try {
      const updated = await intric.spaces.get(get(currentSpace));
      currentSpace.set(updated);
      return updated;
    } catch (e) {
      console.error("Error updating current space", e);
    }
  }

  /** Will create a new space and return it on success. Will return null on failure and show an alert */
  async function createSpace(space: { name: string }) {
    try {
      const newSpace = await intric.spaces.create({ name: space.name });
      refreshSpaces();
      return newSpace;
    } catch (e) {
      alert(`Error creating new space ${space.name}`);
      console.error(e);
    }
    return null;
  }

  /** Will update a given space. If no space is specified will update the current space. */
  async function updateSpace(
    update: Parameters<typeof intric.spaces.update>[0]["update"],
    space?: { id: string } | undefined
  ) {
    const { id } = space ?? get(currentSpace);
    try {
      const updatedSpace = await intric.spaces.update({ space: { id }, update });
      userSpaces.update((spaces) => {
        const idx = spaces.findIndex((space) => space.id === updatedSpace.id);
        if (idx > -1) {
          spaces[idx] = updatedSpace;
        }
        return spaces;
      });
      // Only update current if no other space was given
      if (space === undefined) {
        currentSpace.set(updatedSpace);
      }
      return updatedSpace;
    } catch (e) {
      alert(`Error updating space ${id}`);
      console.error(e);
    }
  }

  /** Will delete a given space. Will alert on error. */
  async function deleteSpace(space: { id: string }) {
    try {
      await intric.spaces.delete({ id: space.id });
      await refreshSpaces();
      if (space.id === get(currentSpace).id) {
        goto("/spaces/list");
      }
    } catch (e) {
      alert(`Error deleting space ${space.id}`);
      console.error(e);
    }
  }

  return Object.freeze({
    state: {
      accessibleSpaces: {
        subscribe: userSpaces.subscribe
      },
      currentSpace: derivedCurrentSpace(currentSpace)
    },
    refreshSpaces,
    refreshCurrentSpace,
    createSpace,
    updateSpace,
    deleteSpace,
    watchPageData
  });
}

export { initSpacesManager, getSpacesManager };

function derivedCurrentSpace(space: Readable<Space>) {
  return derived(space, ($space) => {
    // Spreading the $space is less performant than assigning the values
    // But makes type inference much easier. let's keep it like that as
    // long as we do not run into performance issues.
    // At that point we should probably also independently refresh the resources
    // (apps, knowledge) with their respective endpoints.
    return {
      ...$space,
      routeId: $space.personal ? "personal" : $space.id,
      members: $space.members.items,
      applications: {
        assistants: $space.applications.assistants.items,
        services: $space.applications.services.items.filter((service) => {
          return !service.name.startsWith("_intric");
        })
      },
      knowledge: {
        websites: $space.knowledge.websites.items,
        groups: $space.knowledge.groups.items
      },
      hasPermission(action: ResourcePermission, resource: Resource) {
        switch (resource) {
          case "space":
            return $space.permissions?.includes(action) ?? false;
          case "assistant":
            return $space.applications.assistants.permissions?.includes(action) ?? false;
          case "service":
            return $space.applications.services.permissions?.includes(action) ?? false;
          case "collection":
            return $space.knowledge.groups.permissions?.includes(action) ?? false;
          case "website":
            return $space.knowledge.websites.permissions?.includes(action) ?? false;
          case "member":
            return $space.members.permissions?.includes(action) ?? false;
          default:
            return false;
        }
      }
    };
  });
}

type Resource = "space" | "assistant" | "service" | "website" | "collection" | "member";
