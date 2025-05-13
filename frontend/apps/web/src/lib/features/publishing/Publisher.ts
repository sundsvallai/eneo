export type PublishableResource = { id: string; name: string; published?: boolean };

export type PublishableResourceEndpoints = {
  publish: (resource: { id: string }) => Promise<PublishableResource>;
  unpublish: (resource: { id: string }) => Promise<PublishableResource>;
};
