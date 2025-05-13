export const load = async (event) => {
  const { intric } = await event.parent();
  const groupChat = await intric.groupChats.get({ id: event.params.groupChatId });
  return { groupChat };
};
