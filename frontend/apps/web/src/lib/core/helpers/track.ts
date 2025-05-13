/**
 * Identity function returning the arguments
 *
 * Svelte offers an untrack function to not track state in an $effect. However, sometime you want to do the opposite,
 * to track a specific variable without using it in an effect.
 *
 * @example
 * ```
 *  $effect(() => {
 *   track(chat.partner, chat.currentConversation);
 *   focusMentionInput();
 * });
 * ```
 * */
export function track(...args: unknown[]) {
  return args;
}
