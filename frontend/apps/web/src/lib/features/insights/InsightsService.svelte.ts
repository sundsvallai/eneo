/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

import { browser } from "$app/environment";
import { PAGINATION } from "$lib/core/constants";
import { createAsyncState } from "$lib/core/helpers/createAsyncState.svelte";
import { createClassContext } from "$lib/core/helpers/createClassContext";
import { getIntric } from "$lib/core/Intric";
import { CalendarDate } from "@internationalized/date";
import type { ChatPartner, Conversation, ConversationSparse, Intric } from "@intric/intric-js";

class InsightsService {
  #intric: Intric;
  /** General data range for all insight requests */
  dateRange: { start: CalendarDate | undefined; end: CalendarDate | undefined } = $state()!;
  /** Last chat partner */
  #chatPartner: ChatPartner = $state()!;
  /** Some basic statistics */
  statistics: ReturnType<Intric["analytics"]["insights"]["statistics"]> = $state()!;
  // Conversation handling
  #nextCursor = $state<string | undefined>(undefined);
  /** Conversations to explore */
  conversations: ConversationSparse[] = $state([]);
  totalConversationCount = $state(0);
  hasMoreConversations = $derived(this.conversations.length < this.totalConversationCount);
  /** Currently previewed conversation */
  previewedConversation = $state<Conversation | null>(null);
  // Handling to ask some stuff
  question = $state("");
  answer = $state("");

  constructor(intric = getIntric(), chatPartner: () => ChatPartner) {
    this.#intric = intric;

    const now = new Date();
    const today = new CalendarDate(now.getFullYear(), now.getMonth() + 1, now.getUTCDate());

    this.dateRange = {
      start: today.subtract({ days: 30 }),
      end: today
    };

    $effect(() => {
      this.#chatPartner = chatPartner();
      this.previewedConversation = null;
      this.answer = "";
      this.question = "";
      this.#updateStatistics(this.dateRange);
      this.#updateConversations(this.dateRange);
    });
  }

  async #updateStatistics(timeframe: {
    start: CalendarDate | undefined;
    end: CalendarDate | undefined;
  }) {
    // Should only run during effect by default, but let's prevent this being called on the server.
    if (!browser) return;

    if (timeframe.start && timeframe.end) {
      this.statistics = this.#intric.analytics.insights.statistics({
        chatPartner: this.#chatPartner,
        startDate: timeframe?.start?.toString(),
        // We add one day so the end day includes the whole day. otherwise this would be interpreted as 00:00
        endDate: timeframe?.end?.add({ days: 1 }).toString()
      });
    }
  }

  async #updateConversations(
    timeframe: { start: CalendarDate | undefined; end: CalendarDate | undefined },
    append = false
  ) {
    // Should only run during effect by default, but let's prevent this being called on the server.
    if (!browser) return;

    if (timeframe.start && timeframe.end) {
      const conversations = await this.#intric.analytics.insights.conversations.list({
        chatPartner: this.#chatPartner,
        startDate: timeframe?.start?.toString(),
        // We add one day so the end day includes the whole day. otherwise this would be interpreted as 00:00
        endDate: timeframe?.end?.add({ days: 1 }).toString(),
        nextCursor: append ? this.#nextCursor : undefined,
        limit: PAGINATION.PAGE_SIZE
      });

      if (append) {
        this.conversations = [...this.conversations, ...conversations.items];
      } else {
        this.conversations = conversations.items;
      }

      this.#nextCursor = conversations.next_cursor ?? undefined;
      this.totalConversationCount = conversations.total_count;
    }
  }

  loadMoreConversations = createAsyncState(async () => {
    await this.#updateConversations(this.dateRange, true);
  });

  loadConversationPreview = createAsyncState(async (conversation: { id: string }) => {
    this.previewedConversation =
      await this.#intric.analytics.insights.conversations.get(conversation);
  });

  askQuestion = createAsyncState(async (question: string) => {
    this.answer = "";
    this.question = question;

    const response = await this.#intric.analytics.insights.ask({
      startDate: this.dateRange.start?.toString(),
      // We add one day so the end day includes the whole day. otherwise this would be interpreted as 00:00
      endDate: this.dateRange.end?.add({ days: 1 }).toString(),
      chatPartner: this.#chatPartner,
      question,
      onAnswer: (answer) => {
        this.answer += answer;
      }
    });

    this.answer = response.answer;
  });
}

export const [getInsightsService, initInsightsService] = createClassContext(
  "Insights service",
  InsightsService
);
