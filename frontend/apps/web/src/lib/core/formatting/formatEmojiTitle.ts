const leadingEmoji = /^(\p{Extended_Pictographic}|\p{Emoji_Component}|\p{Emoji_Modifier}| )+/u;

export function formatEmojiTitle(title: string) {
  return title.replace(leadingEmoji, "");
}
