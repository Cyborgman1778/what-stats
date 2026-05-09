<template>
  <div class="summary-stack">
    <q-banner rounded class="summary-status">
      <template #avatar>
        <q-icon name="task_alt" />
      </template>
      {{ stats.message }}
    </q-banner>

    <div class="row q-col-gutter-md">
      <div class="col-12 col-sm-6 col-lg-3">
        <MetricCard icon="forum" eyebrow="Mensajes" :value="formatNumber(stats.total_messages)" label="total" />
      </div>

      <div class="col-12 col-sm-6 col-lg-3">
        <MetricCard icon="group" eyebrow="Usuarios" :value="formatNumber(stats.total_users)" label="detectados" />
      </div>

      <div class="col-12 col-sm-6 col-lg-3">
        <MetricCard icon="badge" eyebrow="Participantes" :value="formatNumber(stats.participants.length)" label="nombres" />
      </div>

      <div class="col-12 col-sm-6 col-lg-3">
        <MetricCard icon="verified" eyebrow="Estado" value="OK" label="backend" />
      </div>
    </div>

    <q-card v-if="fileName || analyzedAt" flat class="soft-card summary-file">
      <q-card-section class="row q-col-gutter-md">
        <div v-if="fileName" class="col-12 col-md-4">
          <div class="text-muted">Archivo</div>
          <div class="text-weight-bold ellipsis">{{ fileName }}</div>
        </div>

        <div v-if="fileSize" class="col-12 col-md-4">
          <div class="text-muted">Tamaño</div>
          <div class="text-weight-bold">{{ formatBytes(fileSize) }}</div>
        </div>

        <div v-if="analyzedAt" class="col-12 col-md-4">
          <div class="text-muted">Fecha</div>
          <div class="text-weight-bold">{{ formatDateTime(analyzedAt) }}</div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import MetricCard from 'components/common/MetricCard.vue';
import type { ChatStatsPayload } from 'src/services/api/types';
import { formatBytes, formatNumber } from 'src/utils/format';
import { formatDateTime } from 'src/utils/dates';

defineProps<{
  stats: ChatStatsPayload;
  fileName?: string | undefined;
  fileSize?: number | undefined;
  analyzedAt?: string | undefined;
}>();
</script>

<style scoped lang="scss">
.summary-stack {
  display: grid;
  gap: 16px;
}

.summary-status {
  color: var(--ws-text);
  background: color-mix(in srgb, var(--ws-accent) 10%, var(--ws-surface));
  border: 1px solid color-mix(in srgb, var(--ws-accent) 28%, var(--ws-border));
}

.summary-status .q-icon {
  color: var(--ws-accent-strong);
}

.summary-file {
  color: var(--ws-text);
  background: var(--ws-summary-file-background);
}
</style>
