<template>
  <div class="summary-stack">
    <div class="summary-grid">
      <div class="summary-grid__item">
        <MetricCard icon="forum" eyebrow="Mensajes Totales" :value="formatNumber(stats.total_messages)" />
      </div>

      <div class="summary-grid__item">
        <MetricCard icon="group" eyebrow="Usuarios" :value="formatNumber(stats.total_users)" />
      </div>

      <div class="summary-grid__item">
        <MetricCard icon="database" eyebrow="Tamaño" :value="chatSize" />
      </div>

      <div class="summary-grid__item summary-grid__item--wide">
        <MetricCard icon="event" eyebrow="Inicio del chat" :value="chatStartDate" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import MetricCard from 'components/common/MetricCard.vue';
import type { ChatStatsPayload } from 'src/services/api/types';
import { formatBytes, formatNumber } from 'src/utils/format';
import { compareOptionalDates, parseDDMMYYYY } from 'src/utils/dates';

const props = defineProps<{
  stats: ChatStatsPayload;
  fileSize?: number | undefined;
}>();

const chatSize = computed(() => (typeof props.fileSize === 'number' ? formatBytes(props.fileSize) : '—'));
const chatStartDate = computed(() => formatFirstChatDate(props.stats.messages_per_day));

function formatFirstChatDate(messagesPerDay: Record<string, number>) {
  const firstDay = Object.keys(messagesPerDay)
    .filter((day) => Number.isFinite(messagesPerDay[day]))
    .sort((a, b) => {
      const compared = compareOptionalDates(parseDDMMYYYY(a), parseDDMMYYYY(b));
      return compared === 0 ? a.localeCompare(b, 'es') : compared;
    })[0];

  if (!firstDay) return '—';

  const parsedDate = parseDDMMYYYY(firstDay);

  if (!parsedDate) return firstDay;

  return formatCompactDate(parsedDate);
}

function formatCompactDate(date: Date) {
  const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
  const day = date.getDate();
  const month = months[date.getMonth()] ?? '';

  return `${day} ${month} ${date.getFullYear()}`;
}
</script>

<style scoped lang="scss">
.summary-stack {
  display: grid;
  gap: 16px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 150px), 1fr));
  grid-auto-rows: 1fr;
  gap: 16px;
  align-items: stretch;
}

.summary-grid__item {
  height: 100%;
}

.summary-grid__item--wide {
  grid-column: span 2;
}

@media (max-width: 420px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
