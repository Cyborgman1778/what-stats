import { computed, ref } from 'vue';
import { Notify } from 'quasar';
import { useAnalysisStore } from 'stores/analysis-store';
import { validateChatFile } from 'src/utils/files';
import type { ChatStatsPayload } from 'src/services/api/types';
import type { NormalizedApiError } from 'src/services/api/api-errors';

export function useChatUpload() {
  const analysisStore = useAnalysisStore();

  const selectedFile = ref<File | null>(null);
  const isDragging = ref(false);

  const validation = computed(() => validateChatFile(selectedFile.value));
  const fileError = computed(() => (validation.value.valid ? '' : validation.value.message ?? ''));
  const canSubmit = computed(
    () =>
      validation.value.valid &&
      !analysisStore.isAnalyzing &&
      analysisStore.cooldownRemainingSeconds === 0
  );

  function setFile(file: File | null) {
    selectedFile.value = file;
    analysisStore.clearError();
  }

  function clearSelection() {
    selectedFile.value = null;
  }

  function onDrop(event: DragEvent) {
    isDragging.value = false;
    const file = event.dataTransfer?.files?.[0] ?? null;
    setFile(file);
  }

  async function submit(): Promise<ChatStatsPayload | null> {
    const currentValidation = validateChatFile(selectedFile.value);

    if (!currentValidation.valid || !selectedFile.value) {
      Notify.create({
        type: 'warning',
        message: currentValidation.message ?? 'Selecciona un archivo válido.'
      });

      return null;
    }

    try {
      return await analysisStore.analyzeFile(selectedFile.value);
    } catch (error) {
      const normalizedError = error as NormalizedApiError;

      Notify.create({
        type: 'negative',
        message: normalizedError.userMessage,
        timeout: 8000,
        actions: [{ icon: 'close', color: 'white' }]
      });

      return null;
    }
  }

  return {
    selectedFile,
    isDragging,
    fileError,
    canSubmit,
    setFile,
    clearSelection,
    onDrop,
    submit
  };
}