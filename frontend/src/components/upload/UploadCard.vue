<template>
  <q-card flat class="premium-card upload-card">
    <q-card-section class="upload-card__head">
      <div>
        <div class="upload-card__eyebrow">upload</div>
        <h2 class="upload-card__title">Analizar chat</h2>
      </div>

      <q-chip dense class="secure-chip" icon="lock" label="secured" />
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
          <div class="drop-zone__visual" aria-hidden="true">
            <div class="drop-zone__icon">
              <q-icon name="upload_file" size="34px" />
            </div>
            <div>
              <div class="drop-zone__title">Arrastra tu chat aquí</div>
              <div class="drop-zone__text">Exportación de WhatsApp en .txt o .zip</div>
            </div>
          </div>

          <q-file
            :model-value="selectedFile"
            class="drop-zone__input"
            outlined
            clearable
            counter
            accept=".txt,.zip"
            label="Seleccionar archivo"
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
            class="upload-actions__analyze"
            unelevated
            color="primary"
            type="submit"
            icon="analytics"
            label="Analizar"
            :loading="analysisStore.isAnalyzing"
            :disable="!canSubmit"
          />

          <q-btn
            class="upload-actions__change"
            flat
            color="primary"
            icon="restart_alt"
            label="Cambiar"
            :disable="analysisStore.isAnalyzing || !selectedFile"
            @click="clearSelection"
          />
        </div>

        <q-expansion-item
          class="advanced-options"
          icon="tune"
          label="Opciones avanzadas"
          expand-icon="keyboard_arrow_down"
        >
          <div class="advanced-options__body">
            <q-toggle
              v-model="anonymizeUsers"
              color="primary"
              :disable="analysisStore.isAnalyzing"
              label="Anonimización de usuarios"
            />

            <p>
              Cambia todos los participantes por Usuario 1, Usuario 2, etc. antes de mostrar las estadísticas.
            </p>
          </div>
        </q-expansion-item>
      </q-form>
    </q-card-section>

    <q-inner-loading :showing="analysisStore.isAnalyzing">
      <q-spinner-grid color="primary" size="40px" />
      <div class="q-mt-sm text-weight-medium">Procesando</div>
    </q-inner-loading>
  </q-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useChatUpload } from 'src/composables/useChatUpload';
import { useAnalysisStore } from 'stores/analysis-store';
import type { ChatStatsPayload } from 'src/services/api/types';
import { formatBytes } from 'src/utils/format';

const emit = defineEmits<{
  completed: [stats: ChatStatsPayload];
}>();

const analysisStore = useAnalysisStore();
const anonymizeUsers = ref(false);

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
  const stats = await submit({ anonymizeUsers: anonymizeUsers.value });

  if (stats) {
    emit('completed', stats);
  }
}
</script>

<style scoped lang="scss">
.upload-card {
  position: relative;
  overflow: hidden;
  min-height: 100%;
}

.upload-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--ws-panel-glow);
  pointer-events: none;
}

.upload-card__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.upload-card__eyebrow {
  color: var(--ws-accent-strong);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.upload-card__title {
  margin: 4px 0 0;
  color: var(--ws-text);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
}

.secure-chip {
  color: #ffffff;
  background: linear-gradient(135deg, var(--ws-accent), #00c2ff 48%, #2f6dff);
  border: 1px solid color-mix(in srgb, #ffffff 28%, var(--ws-accent));
  border-radius: 999px;
  box-shadow: 0 12px 30px rgba(21, 151, 255, 0.28);
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.secure-chip :deep(.q-icon) {
  color: #dff5ff;
}

.drop-zone {
  display: grid;
  min-height: 270px;
  align-content: center;
  gap: 22px;
  padding: clamp(22px, 4vw, 34px);
  text-align: center;
  background: var(--ws-dropzone-background);
  border: 1px dashed color-mix(in srgb, var(--ws-accent) 36%, var(--ws-border));
  border-radius: 28px;
  transition: border-color 0.16s ease, background 0.16s ease, transform 0.16s ease;
}

.drop-zone--active {
  transform: translateY(-2px);
  background: var(--ws-dropzone-active-background);
  border-color: var(--ws-accent);
}

.drop-zone__visual {
  display: grid;
  justify-items: center;
  gap: 14px;
}

.drop-zone__icon {
  display: grid;
  place-items: center;
  width: 78px;
  height: 78px;
  color: var(--ws-accent-strong);
  background: var(--ws-dropzone-icon-background);
  border: 1px solid var(--ws-dropzone-icon-border);
  border-radius: 50%;
  box-shadow: var(--ws-dropzone-icon-shadow);
}

.drop-zone__title {
  color: var(--ws-text);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
}

.drop-zone__text {
  margin-top: 5px;
  color: var(--ws-text-muted);
  font-size: 0.88rem;
}

.drop-zone__input {
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
  text-align: left;
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
  background: color-mix(in srgb, var(--ws-danger) 9%, var(--ws-surface-muted));
}

.warning-banner {
  border-color: color-mix(in srgb, var(--ws-attention) 35%, var(--ws-border));
}

.advanced-options {
  overflow: hidden;
  color: var(--ws-text);
  background: color-mix(in srgb, var(--ws-surface-muted) 48%, transparent);
  border: 1px solid var(--ws-border-muted);
  border-radius: 20px;
}

.advanced-options :deep(.q-item) {
  min-height: 48px;
  color: var(--ws-text);
  padding: 10px 14px;
}

.advanced-options :deep(.q-item__section--avatar) {
  min-width: 34px;
  color: var(--ws-accent-strong);
}

.advanced-options__body {
  display: grid;
  gap: 6px;
  padding: 0 14px 14px;
}

.advanced-options__body p {
  margin: 0;
  color: var(--ws-text-muted);
  font-size: 0.82rem;
  line-height: 1.5;
}

.upload-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.upload-actions__analyze {
  min-width: 190px;
  min-height: 48px;
  padding-right: 22px;
  padding-left: 22px;
  font-size: 1rem;
}

.upload-actions__change {
  min-height: 42px;
}

@media (max-width: 560px) {
  .upload-actions .q-btn {
    flex: 1 1 100%;
  }
}
</style>
