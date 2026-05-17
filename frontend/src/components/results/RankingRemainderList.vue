<template>
  <q-list bordered separator class="ranking-remainder-list">
    <q-item
      v-for="entry in entries"
      :key="getEntryKey(entry)"
      class="ranking-remainder-list__row q-pa-md"
    >
      <q-item-section avatar top class="ranking-remainder-list__rank-section">
        <div class="ranking-remainder-list__rank flex flex-center">
          {{ entry.position }}
        </div>
      </q-item-section>

      <q-item-section class="ranking-remainder-list__content">
        <div class="ranking-remainder-list__meta row items-center justify-between no-wrap q-mb-xs">
          <div class="ranking-remainder-list__name ellipsis">{{ entry.item.label }}</div>
          <div class="ranking-remainder-list__value">{{ getValueLabel(entry.item) }}</div>
        </div>

        <HorizontalBarChart
          v-if="getNumericValue(entry.item) !== null"
          :data="getChartData(entry.item)"
          :height="38"
          :ranking-mode="false"
          :compact="true"
          :max-value="maxValue"
        />

        <div v-else class="ranking-remainder-list__fallback text-muted">
          {{ getValueLabel(entry.item) }}
        </div>

        <div v-if="entry.item.caption" class="ranking-remainder-list__caption ellipsis">
          {{ entry.item.caption }}
        </div>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import HorizontalBarChart from 'components/common/HorizontalBarChart.vue';
import { formatNumber } from 'src/utils/format';
import type { DataPoint } from 'src/utils/records';

interface RankingItem {
  key?: string | number;
  label: string;
  value: string | number;
  caption?: string;
}

interface RankingEntry {
  item: RankingItem;
  position: number;
}

const props = withDefaults(
  defineProps<{
    entries: RankingEntry[];
    unit?: string;
  }>(),
  {
    unit: ''
  }
);

const maxValue = computed(() => {
  const numericValues = props.entries
    .map((entry) => getNumericValue(entry.item))
    .filter((value): value is number => value !== null);

  return Math.max(...numericValues, 1);
});

function getNumericValue(item: RankingItem) {
  const numericValue = typeof item.value === 'number' ? item.value : Number(item.value);

  return Number.isFinite(numericValue) ? numericValue : null;
}

function getChartData(item: RankingItem): DataPoint[] {
  const value = getNumericValue(item) ?? 0;

  return [{ label: item.label, value }];
}

function formatValue(value: string | number) {
  return typeof value === 'number' ? formatNumber(value) : value;
}

function getValueLabel(item: RankingItem) {
  const value = formatValue(item.value);

  return props.unit ? `${value} ${props.unit}` : value;
}

function getEntryKey(entry: RankingEntry) {
  return entry.item.key ?? `${entry.item.label}-${entry.position}`;
}
</script>

<style scoped lang="scss">
.ranking-remainder-list {
  overflow: hidden;
  color: var(--ws-text);
  background: var(--ws-table-inset-background);
  border-color: var(--ws-border);
  border-radius: var(--ws-radius);
}

.ranking-remainder-list__row {
  min-height: 82px;
  color: var(--ws-text);
}

.ranking-remainder-list__rank-section {
  min-width: 44px;
  padding-right: 12px;
}

.ranking-remainder-list__rank {
  width: 34px;
  height: 34px;
  color: var(--ws-text);
  border: 1px solid color-mix(in srgb, var(--ws-accent-strong) 45%, var(--ws-border));
  border-radius: 50%;
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 0.82rem;
  font-weight: 900;
  background: color-mix(in srgb, var(--ws-surface-muted) 58%, transparent);
}

.ranking-remainder-list__content {
  min-width: 0;
}

.ranking-remainder-list__meta {
  gap: 10px;
}

.ranking-remainder-list__name {
  min-width: 0;
  color: var(--ws-text);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 0.88rem;
  font-weight: 800;
}

.ranking-remainder-list__value {
  flex: 0 0 auto;
  color: var(--ws-accent-strong);
  font-size: 0.78rem;
  font-weight: 800;
  white-space: nowrap;
}

.ranking-remainder-list__caption,
.ranking-remainder-list__fallback {
  margin-top: 2px;
  color: var(--ws-text-muted);
  font-size: 0.74rem;
}

@media (max-width: 520px) {
  .ranking-remainder-list__row {
    padding-right: 12px;
    padding-left: 12px;
  }
}
</style>
