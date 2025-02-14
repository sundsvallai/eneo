/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

import { CalendarDate } from "@internationalized/date";
import type { Assistant, AssistantResponse } from "@intric/intric-js";

export const load = async (event) => {
  const { intric } = await event.parent();

  event.depends("insights:assistant");

  const id = event.params.assistantId;
  const now = new Date();
  const today = new CalendarDate(now.getFullYear(), now.getMonth() + 1, now.getUTCDate());
  const includeFollowups = false;

  const [questions, assistant]: [AssistantResponse[], Assistant] = await Promise.all([
    intric.analytics.listQuestions({
      assistant: { id },
      options: {
        start: today.subtract({ days: 30 }).toString(),
        end: today.toString(),
        includeFollowups
      }
    }),
    intric.assistants.get({ id })
  ]);

  return {
    questions,
    assistant,
    timeframe: {
      start: today.subtract({ days: 30 }),
      end: today
    },
    includeFollowups
  };
};
