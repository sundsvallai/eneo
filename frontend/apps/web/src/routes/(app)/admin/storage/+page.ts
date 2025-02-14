/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

export const load = async (event) => {
  const { intric } = await event.parent();

  const spaces = await intric.storage
    .listSpaces()
    .then((spaces) => spaces.sort((a, b) => b.size - a.size));

  return { spaces };
};
