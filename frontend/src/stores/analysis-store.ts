import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import type { AxiosProgressEvent } from 'axios';
import type { ChatStatsPayload } from 'src/services/api/types';
import type { NormalizedApiError } from 'src/services/api/api-errors';
import { uploadChat } from 'src/services/api/whatstats-api';

interface CurrentFileMeta {
  name: string;
  size: number;
  type: string;
  analyzedAt: string;
}

interface AnalyzeFileOptions {
  anonymizeUsers?: boolean;
}

function anonymizeChatStats(stats: ChatStatsPayload): ChatStatsPayload {
  const aliases = new Map<string, string>();

  function getAlias(name: string) {
    const normalizedName = name.trim();
    if (!normalizedName) return name;

    const existingAlias = aliases.get(normalizedName);
    if (existingAlias) return existingAlias;

    const alias = `Usuario ${aliases.size + 1}`;
    aliases.set(normalizedName, alias);

    return alias;
  }

  stats.participants.forEach((participant) => getAlias(participant));
  Object.keys(stats.n_messages_per_user).forEach((participant) => getAlias(participant));
  stats.longest_messages.forEach((message) => getAlias(message.Author));

  const messagesPerAnonymousUser = Object.entries(stats.n_messages_per_user).reduce<Record<string, number>>(
    (accumulator, [participant, count]) => {
      const alias = getAlias(participant);
      accumulator[alias] = (accumulator[alias] ?? 0) + count;

      return accumulator;
    },
    {}
  );

  return {
    ...stats,
    participants: stats.participants.map((participant) => getAlias(participant)),
    n_messages_per_user: messagesPerAnonymousUser,
    longest_messages: stats.longest_messages.map((message) => ({
      ...message,
      Author: getAlias(message.Author)
    }))
  };
}

export const useAnalysisStore = defineStore('analysis', () => {
  const stats = ref<ChatStatsPayload | null>(null);
  const currentFile = ref<CurrentFileMeta | null>(null);
  const isAnalyzing = ref(false);
  const uploadProgress = ref(0);
  const error = ref<NormalizedApiError | null>(null);
  const cooldownUntil = ref<number | null>(null);

  const hasStats = computed(() => stats.value !== null);

  const cooldownRemainingSeconds = computed(() => {
    if (!cooldownUntil.value) return 0;
    return Math.max(0, Math.ceil((cooldownUntil.value - Date.now()) / 1000));
  });

  function clearAnalysis() {
    stats.value = null;
    currentFile.value = null;
    error.value = null;
    uploadProgress.value = 0;
  }

  function clearError() {
    error.value = null;
  }

  async function analyzeFile(file: File, options: AnalyzeFileOptions = {}) {
    if (isAnalyzing.value) return null;

    error.value = null;
    stats.value = null;
    uploadProgress.value = 0;
    isAnalyzing.value = true;

    try {
      const response = await uploadChat(file, (event: AxiosProgressEvent) => {
        if (!event.total) return;
        uploadProgress.value = Math.min(100, Math.round((event.loaded * 100) / event.total));
      });

      const nextStats = options.anonymizeUsers ? anonymizeChatStats(response.stats) : response.stats;

      stats.value = nextStats;
      currentFile.value = {
        name: file.name,
        size: file.size,
        type: file.type || 'Archivo de WhatsApp',
        analyzedAt: new Date().toISOString()
      };

      return nextStats;
    } catch (unknownError) {
      const normalizedError = unknownError as NormalizedApiError;
      error.value = normalizedError;

      if (normalizedError.status === 429) {
        const seconds = normalizedError.retryAfterSeconds ?? 60;
        cooldownUntil.value = Date.now() + seconds * 1000;
      }

      throw normalizedError;
    } finally {
      isAnalyzing.value = false;
      uploadProgress.value = 0;
    }
  }

  return {
    stats,
    currentFile,
    isAnalyzing,
    uploadProgress,
    error,
    cooldownUntil,
    hasStats,
    cooldownRemainingSeconds,
    analyzeFile,
    clearAnalysis,
    clearError
  };
});
