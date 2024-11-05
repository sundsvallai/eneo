/* 
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

export const load = async (event) => {
  const { intric } = await event.parent();

  const [spaces, currentSpace] = await Promise.all([
    intric.spaces.list(),
    intric.spaces.getPersonalSpace()
  ]);

  return { spaces, currentSpace, loadedAt: new Date().toUTCString() };
};
