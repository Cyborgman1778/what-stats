import { computed, type Ref } from 'vue';
import type { ChatStatsPayload, TopStreak } from 'src/services/api/types';
import {
  limitDataPoints,
  sortRecordByDay,
  sortRecordByHour,
  sortRecordByMonth,
  sortRecordByValue,
  sortRecordByYear
} from 'src/utils/records';

export function useNormalizedStats(stats: Ref<ChatStatsPayload | null>) {
  const messagesByUser = computed(() => sortRecordByValue(stats.value?.n_messages_per_user));

  const hotHours = computed(() => sortRecordByHour(stats.value?.hot_hours));

  const messagesPerDay = computed(() => sortRecordByDay(stats.value?.messages_per_day));

  const messagesPerMonth = computed(() => sortRecordByMonth(stats.value?.messages_per_month));

  const messagesPerYear = computed(() => sortRecordByYear(stats.value?.messages_per_year));

  const topMessagesPerDay = computed(() => sortRecordByValue(stats.value?.top_messages_per_day));

  const topWords = computed(() =>
    limitDataPoints(sortRecordByValue(stats.value?.top_words), 20)
  );

  const topEmojis = computed(() =>
    limitDataPoints(sortRecordByValue(stats.value?.top_emojis), 20)
  );

  const longestMessages = computed(() => stats.value?.longest_messages ?? []);

  const topStreaks = computed<TopStreak[]>(() => {
    return [...(stats.value?.top_streaks ?? [])].sort((a, b) => b.duration - a.duration);
  });

  return {
    messagesByUser,
    hotHours,
    messagesPerDay,
    messagesPerMonth,
    messagesPerYear,
    topMessagesPerDay,
    topWords,
    topEmojis,
    longestMessages,
    topStreaks
  };
}