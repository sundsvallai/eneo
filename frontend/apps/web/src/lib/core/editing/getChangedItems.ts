export function getRemovedItems<T extends { id: string }[]>(a: T, b: T) {
  const remainingItemIds = b.map((item) => item.id);
  const removedItems = a.filter((item, index, self) => {
    const wasRemoved = !remainingItemIds.includes(item.id);
    const isUnique = index === self.findIndex((duplicate) => duplicate.id === item.id);
    return wasRemoved && isUnique;
  });
  return removedItems;
}

export function getAddedItems<T extends { id: string }[]>(a: T, b: T) {
  const existingItemIds = a.map((item) => item.id);
  const addedItems = b.filter((item, index, self) => {
    const wasAdded = !existingItemIds.includes(item.id);
    const isUnique = index === self.findIndex((duplicate) => duplicate.id === item.id);
    return wasAdded && isUnique;
  });

  return addedItems;
}
