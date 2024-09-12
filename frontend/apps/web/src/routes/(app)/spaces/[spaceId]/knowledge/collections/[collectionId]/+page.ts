export const load = async (event) => {
  const { intric } = await event.parent();
  const selectedCollectionId = event.params.collectionId;

  event.depends("blobs:list");

  const [group, blobs] = await Promise.all([
    intric.groups.get({ id: selectedCollectionId }),
    intric.groups.listInfoBlobs({ id: selectedCollectionId })
  ]);
  return { collection: group, blobs, selectedCollectionId };
};
