<template>
  <q-list bordered separator class="ranking-list">
    <q-item v-for="(item, index) in data" :key="`${item.label}-${index}`">
      <q-item-section avatar>
        <q-avatar class="ranking-badge" :class="getRankingBadgeClass(index)" size="30px">
          {{ index + 1 }}
        </q-avatar>
      </q-item-section>

      <q-item-section>
        <q-item-label class="ellipsis">{{ item.label }}</q-item-label>
        <q-item-label caption>{{ formatNumber(item.value) }} {{ unit }}</q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script setup lang="ts">
import type { DataPoint } from 'src/utils/records';
import { formatNumber } from 'src/utils/format';

withDefaults(
  defineProps<{
    data: DataPoint[];
    unit?: string;
  }>(),
  {
    unit: 'mensajes'
  }
);

function getRankingBadgeClass(index: number) {
  if (index === 0) return 'ranking-badge--gold';
  if (index === 1) return 'ranking-badge--silver';
  if (index === 2) return 'ranking-badge--bronze';

  return 'ranking-badge--default';
}
</script>

<style scoped lang="scss">
.ranking-list {
  border-color: var(--ws-border);
  border-radius: var(--ws-radius);
  overflow: hidden;
  background: var(--ws-table-inset-background);
}

.ranking-badge {
  color: var(--ws-text);
  background: color-mix(in srgb, var(--ws-surface-muted) 72%, transparent);
  border: 2px solid var(--ws-border);
  font-weight: 800;
  box-shadow: inset 0 0 0 1px color-mix(in srgb, #ffffff 14%, transparent);
}

.ranking-badge--gold {
  border-color: #d6a426;
  box-shadow: 0 0 0 2px color-mix(in srgb, #d6a426 18%, transparent), inset 0 0 0 1px color-mix(in srgb, #fff2b8 42%, transparent);
}

.ranking-badge--silver {
  border-color: #b8c0cc;
  box-shadow: 0 0 0 2px color-mix(in srgb, #b8c0cc 18%, transparent), inset 0 0 0 1px color-mix(in srgb, #ffffff 36%, transparent);
}

.ranking-badge--bronze {
  border-color: #b7783c;
  box-shadow: 0 0 0 2px color-mix(in srgb, #b7783c 18%, transparent), inset 0 0 0 1px color-mix(in srgb, #ffd4a3 32%, transparent);
}

.ranking-badge--default {
  border-color: color-mix(in srgb, var(--ws-text-muted) 46%, var(--ws-border));
}
</style>
