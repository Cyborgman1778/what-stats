<template>
  <q-dialog :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)">
    <q-card class="settings-card">
      <q-card-section class="settings-card__head">
        <div>
          <div class="settings-card__title">Ajustes</div>
          <div class="text-muted">preferencias de la app</div>
        </div>

        <q-btn v-close-popup flat round dense icon="close" aria-label="Cerrar ajustes" />
      </q-card-section>

      <q-separator />

      <q-card-section class="settings-card__body">
        <div class="settings-field">
          <label>Tema</label>
          <q-option-group
            v-model="draftTheme"
            :options="themeOptions"
            color="primary"
            inline
          />
        </div>

        <q-separator />

        <div class="developer-options">
          <q-toggle
            v-model="developerOptionsEnabled"
            color="primary"
            label="Opciones de desarrollador"
          />

          <q-slide-transition>
            <div v-if="developerOptionsEnabled" class="developer-options__body">
              <div class="settings-field">
                <label>Dirección del backend</label>
                <q-input
                  v-model.trim="draftApiBaseUrl"
                  outlined
                  dense
                  placeholder="https://api.whatstats.net"
                  autocomplete="off"
                  :disable="testingConnection"
                >
                  <template #prepend>
                    <q-icon name="dns" />
                  </template>
                </q-input>
              </div>

              <q-btn
                outline
                color="primary"
                icon="wifi_tethering"
                label="Probar conectividad"
                :loading="testingConnection"
                @click="testConnectivity"
              />
            </div>
          </q-slide-transition>
        </div>
      </q-card-section>

      <q-card-actions align="right" class="settings-card__actions">
        <q-btn flat label="Cancelar" v-close-popup />
        <q-btn color="primary" label="Guardar" @click="save" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { Notify } from 'quasar';
import { ref, watch } from 'vue';
import { healthcheck } from 'src/services/api/whatstats-api';
import { usePreferencesStore, type ThemePreference } from 'stores/preferences-store';

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
}>();

const preferencesStore = usePreferencesStore();

const developerOptionsEnabled = ref(false);
const draftApiBaseUrl = ref(preferencesStore.apiBaseUrl);
const draftTheme = ref<ThemePreference>(preferencesStore.theme);
const testingConnection = ref(false);

const themeOptions = [
  { label: 'Claro', value: 'light' },
  { label: 'Oscuro', value: 'dark' },
  { label: 'Auto', value: 'auto' }
];

watch(
  () => props.modelValue,
  (open) => {
    if (!open) return;

    developerOptionsEnabled.value = false;
    draftApiBaseUrl.value = preferencesStore.apiBaseUrl;
    draftTheme.value = preferencesStore.theme;
  }
);

async function testConnectivity() {
  testingConnection.value = true;

  try {
    const response = await healthcheck(draftApiBaseUrl.value);

    Notify.create({
      type: 'positive',
      message: response.message || 'Conectividad correcta.'
    });
  } catch {
    Notify.create({
      type: 'negative',
      message: 'No se pudo conectar con esa dirección.'
    });
  } finally {
    testingConnection.value = false;
  }
}

function save() {
  if (developerOptionsEnabled.value) {
    preferencesStore.setBackendUrl(draftApiBaseUrl.value);
  }

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

.developer-options {
  display: grid;
  gap: 12px;
}

.developer-options__body {
  display: grid;
  gap: 12px;
  padding: 12px;
  background: var(--ws-surface-muted);
  border: 1px solid var(--ws-border-muted);
  border-radius: var(--ws-radius-sm);
}

.developer-options__body .q-btn {
  justify-self: start;
}

.settings-card__actions {
  padding: 12px 16px 16px;
}

</style>
