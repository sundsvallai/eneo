/* 
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

export const load = async (event) => {
  const { intric } = await event.parent();

  event.depends("insights:assistant");

  const id = event.params.assistantId;
  const period = 30;
  const includeFollowups = false;

  const [questions, assistant] = await Promise.all([
    intric.analytics.listQuestions({
      assistant: { id },
      options: { period, includeFollowups }
    }),
    intric.assistants.get({ id })
  ]);

  return {
    questions,
    assistant,
    period,
    includeFollowups
  };
};
