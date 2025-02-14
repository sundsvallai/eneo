import type { EmbeddingModel, GroupSparse, WebsiteSparse } from "@intric/intric-js";

export type AvailableKnowledge = {
  [id: string]: {
    name: string;
    isEnabled: boolean;
    isCompatible: boolean;
    websites: WebsiteSparse[];
    groups: GroupSparse[];
    availableItemsCount: number;
  };
};

export function getAvailableKnowledge(
  space: {
    knowledge: { websites: WebsiteSparse[]; groups: GroupSparse[] };
    embedding_models: EmbeddingModel[];
  },
  selectedWebsites: WebsiteSparse[] | undefined,
  selectedGroups: GroupSparse[] | undefined,
  filterInput?: string
) {
  const matchesFilter = createFilter(filterInput);
  const dominantModelId =
    selectedGroups?.[0]?.embedding_model.id ?? selectedWebsites?.[0]?.embedding_model.id ?? null;
  const selectedWebsiteIds = selectedWebsites?.map((website) => website.id) ?? [];
  const selectedGroupIds = selectedGroups?.map((group) => group.id) ?? [];
  const availableModelIds = space.embedding_models.map((model) => model.id);
  const availableKnowledge: AvailableKnowledge = {};

  if (selectedGroups) {
    space.knowledge.groups.forEach((group) => {
      const isCompatible = dominantModelId ? dominantModelId === group.embedding_model.id : true;

      // Always configure the model, even if not adding a group, so we can show an approporate message
      availableKnowledge[group.embedding_model.id] = availableKnowledge[
        group.embedding_model.id
      ] || {
        name: group.embedding_model.name,
        isEnabled: availableModelIds.includes(group.embedding_model.id),
        isCompatible,
        websites: [],
        groups: [],
        availableItemsCount: 0
      };

      // Now that the model is set up we can exit, same goes for websites below
      if (!isCompatible) return;
      if (selectedGroupIds.includes(group.id)) return;
      if (!matchesFilter(group.name)) return;

      availableKnowledge[group.embedding_model.id].groups.push(group);
      availableKnowledge[group.embedding_model.id].availableItemsCount += 1;
    });
  }

  if (selectedWebsites) {
    space.knowledge.websites.forEach((website) => {
      const isCompatible = dominantModelId ? dominantModelId === website.embedding_model.id : true;

      availableKnowledge[website.embedding_model.id] = availableKnowledge[
        website.embedding_model.id
      ] || {
        name: website.embedding_model.name,
        isEnabled: availableModelIds.includes(website.embedding_model.id),
        isCompatible,
        websites: [],
        groups: [],
        availableItemsCount: 0
      };

      if (!isCompatible) return;
      if (selectedWebsiteIds.includes(website.id)) return;
      // We allow filtering both on the URL and the name, even if only one of them is shown
      if (!(matchesFilter(website.url) || matchesFilter(website.name))) return;

      availableKnowledge[website.embedding_model.id].websites.push(website);
      availableKnowledge[website.embedding_model.id].availableItemsCount += 1;
    });
  }
  return { sections: availableKnowledge, showHeaders: Object.keys(availableKnowledge).length > 1 };
}

function createFilter(filter: string | undefined) {
  if (!filter) {
    return () => true;
  }
  return (data?: string | null) => {
    if (!data) {
      return false;
    }
    return data.toLowerCase().includes(filter.toLowerCase());
  };
}
