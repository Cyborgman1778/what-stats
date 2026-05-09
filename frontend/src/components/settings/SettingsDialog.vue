<template>
  <q-dialog :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)">
    <q-card class="settings-card">
      <q-card-section class="settings-card__head">
        <div>
          <div class="settings-card__title">Ajustes</div>
          <div class="text-muted">backend y tema</div>
        </div>

        <q-btn v-close-popup flat round dense icon="close" aria-label="Cerrar ajustes" />
      </q-card-section>

      <q-separator />

      <q-card-section class="settings-card__body">
        <div class="settings-field">
          <label>API</label>
          <q-input
            v-model.trim="draftApiBaseUrl"
            outlined
            dense
            placeholder="http://127.0.0.1:8000"
            autocomplete="off"
            :disable="testing"
          >
            <template #prepend>
              <q-icon name="dns" />
            </template>
          </q-input>
        </div>

        <div class="settings-field">
          <label>Tema</label>
          <q-option-group
            v-model="draftTheme"
            :options="themeOptions"
            color="primary"
            inline
          />
        </div>

        <q-banner v-if="connectionMessage" rounded class="connection-banner" :class="connectionOk ? 'connection-banner--ok' : 'connection-banner--error'">
          {{ connectionMessage }}
        </q-banner>
      </q-card-section>

      <q-card-actions align="between" class="settings-card__actions">
        <q-btn
          outline
          color="primary"
          icon="wifi_tethering"
          label="Probar"
          :loading="testing"
          @click="testConnection"
        />

        <div class="row q-gutter-sm">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn color="primary" label="Guardar" @click="save" />
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { Notify } from 'quasar';
import { ref, watch } from 'vue';
import { healthcheck } from 'src/services/api/whatstats-api';
import type { NormalizedApiError } from 'src/services/api/api-errors';
import { sanitizeApiBaseUrl } from 'src/utils/config';
import { usePreferencesStore, type ThemePreference } from 'stores/preferences-store';

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
}>();

const preferencesStore = usePreferencesStore();

const draftApiBaseUrl = ref(preferencesStore.apiBaseUrl);
const draftTheme = ref<ThemePreference>(preferencesStore.theme);
const testing = ref(false);
const connectionMessage = ref('');
const connectionOk = ref(false);

const themeOptions = [
  { label: 'Claro', value: 'light' },
  { label: 'Oscuro', value: 'dark' },
  { label: 'Auto', value: 'auto' }
];

watch(
  () => props.modelValue,
  (open) => {
    if (!open) return;

    draftApiBaseUrl.value = preferencesStore.apiBaseUrl;
    draftTheme.value = preferencesStore.theme;
    connectionMessage.value = '';
    connectionOk.value = false;
  }
);

async function testConnection() {
  testing.value = true;
  connectionMessage.value = '';
  connectionOk.value = false;

  try {
    const response = await healthcheck(sanitizeApiBaseUrl(draftApiBaseUrl.value));
    connectionOk.value = true;
    connectionMessage.value = response.message;
  } catch (error) {
    const normalized = error as NormalizedApiError;
    connectionOk.value = false;
    connectionMessage.value = normalized.userMessage;
  } finally {
    testing.value = false;
  }
}

function save() {
  preferencesStore.setBackendUrl(draftApiBaseUrl.value);
  preferencesStore.setTheme(draftTheme.value);

  Notify.create({
    type: 'positive',
    message: 'Ajustes guardados.'
  });

  emit('update:modelValue', false);
}
</script>

<style scoped lang="scss">
.settings-card {
  width: min(560px, calc(100vw - 24px));
  color: var(--ws-text);
  background: var(--ws-surface);
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  box-shadow: var(--ws-shadow-floating);
}

.settings-card__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.settings-card__title {
  color: var(--ws-text);
  font-size: 1.08rem;
  font-weight: 700;
}

.settings-card__body {
  display: grid;
  gap: 18px;
}

.settings-field {
  display: grid;
  gap: 8px;
}

.settings-field label {
  color: var(--ws-text-muted);
  font-size: 0.82rem;
  font-weight: 600;
}

.settings-card__actions {
  padding: 12px 16px 16px;
}

.connection-banner {
  color: var(--ws-text);
  background: var(--ws-surface-muted);
  border: 1px solid var(--ws-border);
}

.connection-banner--ok {
  border-color: color-mix(in srgb, var(--ws-success) 35%, var(--ws-border));
}

.connection-banner--error {
  border-color: color-mix(in srgb, var(--ws-danger) 35%, var(--ws-border));
}
</style>
