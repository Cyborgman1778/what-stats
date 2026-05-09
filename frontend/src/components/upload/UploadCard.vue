<template>
  <q-card flat class="premium-card upload-card">
    <q-card-section class="upload-card__head">
      <div>
        <div class="upload-card__eyebrow">upload</div>
        <h2 class="upload-card__title">Analizar chat</h2>
      </div>

      <q-chip dense class="ws-chip" icon="lock" label="local" />
    </q-card-section>

    <q-separator />

    <q-card-section>
      <q-form class="q-gutter-md" @submit.prevent="handleSubmit">
        <div
          class="drop-zone"
          :class="{ 'drop-zone--active': isDragging }"
          @dragenter.prevent="isDragging = true"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="onDrop"
        >
          <q-file
            :model-value="selectedFile"
            outlined
            clearable
            counter
            accept=".txt,.zip"
            label=".txt o .zip"
            :disable="analysisStore.isAnalyzing"
            :error="selectedFile !== null && Boolean(fileError)"
            :error-message="fileError"
            @update:model-value="setFile"
          >
            <template #prepend>
              <q-icon name="upload_file" />
            </template>
            <template #hint>
              máximo 50 MB
            </template>
          </q-file>

          <div class="drop-zone__hint">arrastra o selecciona archivo</div>
        </div>

        <q-banner v-if="selectedFile && !fileError" rounded class="file-banner">
          <template #avatar>
            <q-icon name="description" />
          </template>
          <span class="ellipsis">{{ selectedFile.name }}</span>
          <span class="text-muted">{{ formatBytes(selectedFile.size) }}</span>
        </q-banner>

        <q-banner v-if="analysisStore.error" rounded class="error-banner">
          <template #avatar>
            <q-icon name="error" />
          </template>

          <div>
            <div class="text-weight-bold">{{ analysisStore.error.userMessage }}</div>
            <ul v-if="analysisStore.error.troubleshooting?.length" class="q-mb-none q-pl-md">
              <li v-for="tip in analysisStore.error.troubleshooting" :key="tip">
                {{ tip }}
              </li>
            </ul>
          </div>
        </q-banner>

        <q-banner v-if="analysisStore.cooldownRemainingSeconds > 0" rounded class="warning-banner">
          Espera {{ analysisStore.cooldownRemainingSeconds }} s.
        </q-banner>

        <div v-if="analysisStore.isAnalyzing" class="q-gutter-sm">
          <div class="row items-center justify-between text-muted">
            <span>Analizando</span>
            <span v-if="analysisStore.uploadProgress > 0 && analysisStore.uploadProgress < 100">
              {{ analysisStore.uploadProgress }} %
            </span>
          </div>

          <q-linear-progress
            rounded
            size="8px"
            color="primary"
            :value="analysisStore.uploadProgress / 100"
            :indeterminate="analysisStore.uploadProgress === 0 || analysisStore.uploadProgress >= 100"
          />
        </div>

        <div class="upload-actions">
          <q-btn
            unelevated
            color="primary"
            type="submit"
            icon="analytics"
            label="Analizar"
            :loading="analysisStore.isAnalyzing"
            :disable="!canSubmit"
          />

          <q-btn
            flat
            color="primary"
            icon="restart_alt"
            label="Cambiar"
            :disable="analysisStore.isAnalyzing || !selectedFile"
            @click="clearSelection"
          />
        </div>
      </q-form>
    </q-card-section>

    <q-inner-loading :showing="analysisStore.isAnalyzing">
      <q-spinner-grid color="primary" size="40px" />
      <div class="q-mt-sm text-weight-medium">Procesando</div>
    </q-inner-loading>
  </q-card>
</template>

<script setup lang="ts">
import { useChatUpload } from 'src/composables/useChatUpload';
import { useAnalysisStore } from 'stores/analysis-store';
import type { ChatStatsPayload } from 'src/services/api/types';
import { formatBytes } from 'src/utils/format';

const emit = defineEmits<{
  completed: [stats: ChatStatsPayload];
}>();

const analysisStore = useAnalysisStore();

const {
  selectedFile,
  isDragging,
  fileError,
  canSubmit,
  setFile,
  clearSelection,
  onDrop,
  submit
} = useChatUpload();

async function handleSubmit() {
  const stats = await submit();

  if (stats) {
    emit('completed', stats);
  }
}
</script>

<style scoped lang="scss">
.upload-card {
  position: relative;
  overflow: hidden;
}

.upload-card__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.upload-card__eyebrow {
  color: var(--ws-text-subtle);
  font-family: ui-monospace, SFMono-Regular, SF Mono, Consolas, Liberation Mono, monospace;
  font-size: 0.72rem;
  text-transform: uppercase;
}

.upload-card__title {
  margin: 4px 0 0;
  font-size: 1.35rem;
  font-weight: 700;
}

.drop-zone {
  padding: 16px;
  background: var(--ws-canvas-subtle);
  border: 1px dashed var(--ws-border);
  border-radius: var(--ws-radius);
  transition: border-color 0.16s ease, background 0.16s ease;
}

.drop-zone--active {
  background: color-mix(in srgb, var(--ws-success) 7%, var(--ws-canvas-subtle));
  border-color: var(--ws-success);
}

.drop-zone__hint {
  margin-top: 8px;
  color: var(--ws-text-muted);
  font-size: 0.82rem;
}

.file-banner,
.warning-banner,
.error-banner {
  color: var(--ws-text);
  background: var(--ws-surface-muted);
  border: 1px solid var(--ws-border);
}

.file-banner :deep(.q-banner__content) {
  display: flex;
  min-width: 0;
  gap: 10px;
}

.error-banner {
  border-color: color-mix(in srgb, var(--ws-danger) 35%, var(--ws-border));
}

.warning-banner {
  border-color: color-mix(in srgb, var(--ws-attention) 35%, var(--ws-border));
}

.upload-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
