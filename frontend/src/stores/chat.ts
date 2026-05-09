import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { ChatStatsPayload } from 'src/types';

export const useChatStore = defineStore('chat', () => {
  const currentStats = ref<ChatStatsPayload | null>(null);
  const isLoading = ref(false);

  const setStats = (stats: ChatStatsPayload) => {
    currentStats.value = stats;
  };

  const clearStats = () => {
    currentStats.value = null;
  };

  return { currentStats, isLoading, setStats, clearStats };
});