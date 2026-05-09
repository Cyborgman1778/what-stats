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

  async function analyzeFile(file: File) {
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

      stats.value = response.stats;
      currentFile.value = {
        name: file.name,
        size: file.size,
        type: file.type || 'Archivo de WhatsApp',
        analyzedAt: new Date().toISOString()
      };

      return response.stats;
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