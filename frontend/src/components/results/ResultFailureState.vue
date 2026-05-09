<template>
  <AppEmptyState
    icon="manage_search"
    title="Sin mensajes válidos"
    :message="message"
  >
    <div class="q-gutter-md">
      <q-btn color="primary" unelevated icon="upload_file" label="Analizar otro" @click="emit('analyzeAnother')" />

      <q-card flat class="soft-card text-left q-mt-md">
        <q-list separator>
          <q-expansion-item icon="checklist" label="Revisar">
            <q-card-section class="text-muted">
              <ul class="q-mb-none">
                <li>Sin multimedia.</li>
                <li>.txt o .zip.</li>
                <li>Formato WhatsApp Android/iOS.</li>
              </ul>
            </q-card-section>
          </q-expansion-item>
        </q-list>
      </q-card>
    </div>
  </AppEmptyState>
</template>

<script setup lang="ts">
import AppEmptyState from 'components/common/AppEmptyState.vue';

defineProps<{
  message: string;
}>();

const emit = defineEmits<{
  analyzeAnother: [];
}>();
</script>
