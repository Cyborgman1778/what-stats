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
            :disable="testing || internetTesting"
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

        <q-banner
          v-if="connectionMessage"
          rounded
          class="connection-banner"
          :class="connectionOk ? 'connection-banner--ok' : 'connection-banner--error'"
        >
          <div class="connection-banner__title">Backend</div>
          <div>{{ connectionMessage }}</div>
        </q-banner>

        <q-banner
          v-if="internetMessage"
          rounded
          class="connection-banner"
          :class="internetOk ? 'connection-banner--ok' : 'connection-banner--error'"
        >
          <div class="connection-banner__title">Internet</div>
          <div>{{ internetMessage }}</div>
        </q-banner>

        <q-card flat class="diagnostics-card">
          <div class="diagnostics-card__head">
            <q-icon name="bug_report" size="18px" />
            <span>Diagnóstico</span>
          </div>

          <dl class="diagnostics-list">
            <div>
              <dt>URL API efectiva</dt>
              <dd>{{ effectiveApiBaseUrl }}</dd>
            </div>

            <div>
              <dt>URL guardada</dt>
              <dd>{{ preferencesStore.apiBaseUrl }}</dd>
            </div>

            <div>
              <dt>Plataforma Capacitor</dt>
              <dd>{{ runtimePlatform }} · nativa: {{ isNativeRuntime ? 'sí' : 'no' }}</dd>
            </div>

            <div>
              <dt>HTTP nativo</dt>
              <dd>{{ nativeHttpStatus }}</dd>
            </div>

            <div>
              <dt>Origen WebView</dt>
              <dd>{{ webOrigin }}</dd>
            </div>

            <div v-if="apiDiagnostic.testedUrl">
              <dt>URL probada</dt>
              <dd>{{ apiDiagnostic.testedUrl }}</dd>
            </div>

            <div v-if="apiDiagnostic.status !== null">
              <dt>Status HTTP</dt>
              <dd>{{ apiDiagnostic.status }} {{ apiDiagnostic.statusText }}</dd>
            </div>

            <div v-if="apiDiagnostic.errorCode">
              <dt>Código error</dt>
              <dd>{{ apiDiagnostic.errorCode }}</dd>
            </div>

            <div v-if="apiDiagnostic.errorMessage">
              <dt>Error técnico</dt>
              <dd>{{ apiDiagnostic.errorMessage }}</dd>
            </div>

            <div v-if="apiDiagnostic.responseData">
              <dt>Respuesta backend</dt>
              <dd><pre>{{ apiDiagnostic.responseData }}</pre></dd>
            </div>
          </dl>
        </q-card>
      </q-card-section>

      <q-card-actions align="between" class="settings-card__actions">
        <div class="settings-card__test-actions">
          <q-btn
            outline
            color="primary"
            icon="dns"
            label="Probar API"
            :loading="testing"
            :disable="internetTesting"
            @click="testConnection"
          />

          <q-btn
            outline
            color="primary"
            icon="public"
            label="Probar internet"
            :loading="internetTesting"
            :disable="testing"
            @click="testInternetConnectivity"
          />
        </div>

        <div class="row q-gutter-sm">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn color="primary" label="Guardar" @click="save" />
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import axios from 'axios';
import { Capacitor } from '@capacitor/core';
import { Notify } from 'quasar';
import { computed, reactive, ref, watch } from 'vue';
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
const internetTesting = ref(false);
const connectionMessage = ref('');
const connectionOk = ref(false);
const internetMessage = ref('');
const internetOk = ref(false);

const runtimePlatform = Capacitor.getPlatform();
const isNativeRuntime = Capacitor.isNativePlatform();
const webOrigin = window.location.origin || 'sin origen disponible';

type AndroidHttpBridge = {
  isEnabled?: () => boolean;
};

type WindowWithAndroidHttpBridge = Window & {
  CapacitorHttpAndroidInterface?: AndroidHttpBridge;
};

const INTERNET_TEST_URL = 'https://www.google.com/generate_204';
const INTERNET_TEST_TIMEOUT_MS = 10000;
const API_TEST_TIMEOUT_MS = 10000;

const effectiveApiBaseUrl = computed(() => sanitizeApiBaseUrl(draftApiBaseUrl.value));
const nativeHttpStatus = computed(() => {
  if (!isNativeRuntime) return 'no aplica en web';

  if (runtimePlatform !== 'android') return 'no verificable en esta plataforma';

  const androidHttp = (window as WindowWithAndroidHttpBridge).CapacitorHttpAndroidInterface;

  if (!androidHttp || typeof androidHttp.isEnabled !== 'function') {
    return 'interfaz Android no disponible';
  }

  return androidHttp.isEnabled() ? 'activo' : 'desactivado';
});

const apiDiagnostic = reactive({
  testedUrl: '',
  status: null as number | null,
  statusText: '',
  errorCode: '',
  errorMessage: '',
  responseData: ''
});

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
    internetMessage.value = '';
    internetOk.value = false;
    resetApiDiagnostic();
  }
);

function formatDiagnosticData(data: unknown) {
  if (data === undefined || data === null || data === '') return '';

  const text = typeof data === 'string' ? data : JSON.stringify(data, null, 2);

  return text.length > 1200 ? `${text.slice(0, 1200)}...` : text;
}

function resetApiDiagnostic() {
  apiDiagnostic.testedUrl = '';
  apiDiagnostic.status = null;
  apiDiagnostic.statusText = '';
  apiDiagnostic.errorCode = '';
  apiDiagnostic.errorMessage = '';
  apiDiagnostic.responseData = '';
}

function getHealthcheckUrl(baseUrl: string) {
  return `${sanitizeApiBaseUrl(baseUrl)}/`;
}

async function testConnection() {
  testing.value = true;
  connectionMessage.value = '';
  connectionOk.value = false;
  resetApiDiagnostic();

  const testedUrl = getHealthcheckUrl(draftApiBaseUrl.value);
  apiDiagnostic.testedUrl = testedUrl;

  try {
    const response = await axios.get(testedUrl, {
      headers: {
        Accept: 'application/json'
      },
      timeout: API_TEST_TIMEOUT_MS,
      validateStatus: () => true
    });

    apiDiagnostic.status = response.status;
    apiDiagnostic.statusText = response.statusText;
    apiDiagnostic.responseData = formatDiagnosticData(response.data);

    if (response.status >= 200 && response.status < 300) {
      connectionOk.value = true;
      connectionMessage.value =
        typeof response.data?.message === 'string'
          ? response.data.message
          : `API accesible. HTTP ${response.status}.`;
      return;
    }

    connectionOk.value = false;
    connectionMessage.value = `La API respondió con HTTP ${response.status} ${response.statusText}.`;
  } catch (error) {
    connectionOk.value = false;

    if (axios.isAxiosError(error)) {
      apiDiagnostic.status = error.response?.status ?? null;
      apiDiagnostic.statusText = error.response?.statusText ?? '';
      apiDiagnostic.errorCode = error.code ?? '';
      apiDiagnostic.errorMessage = error.message;
      apiDiagnostic.responseData = formatDiagnosticData(error.response?.data);

      connectionMessage.value = error.response
        ? `Error HTTP ${error.response.status}: ${error.message}`
        : `Sin respuesta HTTP: ${error.code ?? 'NETWORK'} · ${error.message}`;
      return;
    }

    apiDiagnostic.errorMessage = error instanceof Error ? error.message : String(error);
    connectionMessage.value = apiDiagnostic.errorMessage;
  } finally {
    testing.value = false;
  }
}

function getInternetErrorMessage(error: unknown) {
  if (error instanceof DOMException && error.name === 'AbortError') {
    return `Tiempo de espera agotado tras ${INTERNET_TEST_TIMEOUT_MS / 1000} s.`;
  }

  if (error instanceof TypeError) {
    return `Error de red: ${error.message || 'no se pudo alcanzar el servidor externo.'}`;
  }

  if (error instanceof Error) {
    return `${error.name}: ${error.message}`;
  }

  return String(error);
}

async function testInternetConnectivity() {
  internetTesting.value = true;
  internetMessage.value = '';
  internetOk.value = false;

  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), INTERNET_TEST_TIMEOUT_MS);

  try {
    await fetch(`${INTERNET_TEST_URL}?t=${Date.now()}`, {
      cache: 'no-store',
      mode: 'no-cors',
      signal: controller.signal
    });

    internetOk.value = true;
    internetMessage.value = 'Conectividad externa correcta. Se pudo alcanzar Google.';
  } catch (error) {
    internetOk.value = false;
    internetMessage.value = getInternetErrorMessage(error);
  } finally {
    window.clearTimeout(timeoutId);
    internetTesting.value = false;
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

.settings-card__test-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.connection-banner {
  color: var(--ws-text);
  background: var(--ws-surface-muted);
  border: 1px solid var(--ws-border);
}

.connection-banner__title {
  margin-bottom: 3px;
  color: var(--ws-text);
  font-weight: 700;
}

.connection-banner--ok {
  border-color: color-mix(in srgb, var(--ws-success) 35%, var(--ws-border));
}

.connection-banner--error {
  border-color: color-mix(in srgb, var(--ws-danger) 35%, var(--ws-border));
}

.diagnostics-card {
  display: grid;
  gap: 12px;
  padding: 14px;
  color: var(--ws-text);
  background: color-mix(in srgb, var(--ws-surface-muted) 58%, transparent);
  border: 1px solid var(--ws-border-muted);
  border-radius: var(--ws-radius-sm);
}

.diagnostics-card__head {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--ws-text);
  font-weight: 700;
}

.diagnostics-card__head .q-icon {
  color: var(--ws-accent-strong);
}

.diagnostics-list {
  display: grid;
  gap: 9px;
  margin: 0;
}

.diagnostics-list div {
  min-width: 0;
}

.diagnostics-list dt {
  color: var(--ws-text-subtle);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.diagnostics-list dd {
  min-width: 0;
  margin: 3px 0 0;
  overflow-wrap: anywhere;
  color: var(--ws-text);
  font-size: 0.84rem;
}

.diagnostics-list pre {
  max-height: 160px;
  margin: 0;
  overflow: auto;
  white-space: pre-wrap;
  color: var(--ws-text);
  font-family: ui-monospace, SFMono-Regular, SF Mono, Consolas, Liberation Mono, monospace;
}
</style>
