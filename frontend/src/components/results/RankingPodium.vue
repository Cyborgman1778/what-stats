<template>
  <div class="ranking-podium">
    <div
      v-if="podiumEntries.length > 0"
      class="ranking-podium__stage"
      :class="`ranking-podium__stage--${podiumEntries.length}`"
    >
      <article
        v-for="entry in podiumEntries"
        :key="getEntryKey(entry)"
        class="ranking-podium__item"
        :class="[
          `ranking-podium__item--rank-${entry.position}`,
          { 'ranking-podium__item--selectable': selectable }
        ]"
        :role="selectable ? 'button' : undefined"
        :tabindex="selectable ? 0 : undefined"
        @click="selectEntry(entry)"
        @keydown.enter.prevent="selectEntry(entry)"
        @keydown.space.prevent="selectEntry(entry)"
      >
        <RankingMedal :position="entry.position" :variant="getMedalVariant(entry.position)" size="podium" />

        <div class="ranking-podium__body">
          <div class="ranking-podium__value">
            <span>{{ formatValue(entry.item.value) }}</span>
            <small v-if="unit">{{ unit }}</small>
          </div>

          <div class="ranking-podium__label">{{ entry.item.label }}</div>
          <div v-if="entry.item.caption" class="ranking-podium__caption">{{ entry.item.caption }}</div>
        </div>

        <div class="ranking-podium__base">
          <span>{{ entry.position }}</span>
        </div>
      </article>
    </div>

    <q-list v-if="listEntries.length > 0" bordered separator class="ranking-list">
      <q-item v-for="entry in listEntries" :key="getEntryKey(entry)">
        <q-item-section avatar>
          <RankingMedal :position="entry.position" variant="muted" size="list" />
        </q-item-section>

        <q-item-section>
          <q-item-label class="ellipsis">{{ entry.item.label }}</q-item-label>
          <q-item-label caption>{{ getValueLabel(entry.item) }}</q-item-label>
          <q-item-label v-if="entry.item.caption" caption class="ranking-list__caption">
            {{ entry.item.caption }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import RankingMedal from 'components/results/RankingMedal.vue';
import { formatNumber } from 'src/utils/format';

interface RankingPodiumItem {
  key?: string | number;
  label: string;
  value: string | number;
  caption?: string;
}

interface RankingEntry {
  item: RankingPodiumItem;
  position: number;
}

const props = withDefaults(
  defineProps<{
    items: RankingPodiumItem[];
    unit?: string;
    selectable?: boolean;
  }>(),
  {
    unit: '',
    selectable: false
  }
);

const emit = defineEmits<{
  select: [item: RankingPodiumItem, position: number];
}>();

const rankedEntries = computed<RankingEntry[]>(() =>
  props.items.map((item, index) => ({
    item,
    position: index + 1
  }))
);

const podiumEntries = computed<RankingEntry[]>(() => {
  const topEntries = rankedEntries.value.slice(0, 3);
  const visualOrder = [2, 1, 3];

  return visualOrder
    .map((position) => topEntries.find((entry) => entry.position === position))
    .filter((entry): entry is RankingEntry => Boolean(entry));
});

const listEntries = computed(() => rankedEntries.value.slice(3));

function formatValue(value: string | number) {
  return typeof value === 'number' ? formatNumber(value) : value;
}

function getValueLabel(item: RankingPodiumItem) {
  const value = formatValue(item.value);

  return props.unit ? `${value} ${props.unit}` : value;
}

function getMedalVariant(position: number): 'gold' | 'silver' | 'bronze' | 'muted' {
  if (position === 1) return 'gold';
  if (position === 2) return 'silver';
  if (position === 3) return 'bronze';

  return 'muted';
}

function getEntryKey(entry: RankingEntry) {
  return entry.item.key ?? `${entry.item.label}-${entry.position}`;
}

function selectEntry(entry: RankingEntry) {
  if (!props.selectable) return;

  emit('select', entry.item, entry.position);
}
</script>

<style scoped lang="scss">
.ranking-podium {
  display: grid;
  gap: 18px;
}

.ranking-podium__stage {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  align-items: end;
  gap: clamp(8px, 2vw, 14px);
  min-height: 238px;
}

.ranking-podium__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
  color: var(--ws-text);
  outline: none;
}

.ranking-podium__item--selectable {
  cursor: pointer;
}

.ranking-podium__item--selectable:focus-visible .ranking-podium__body,
.ranking-podium__item--selectable:hover .ranking-podium__body {
  border-color: color-mix(in srgb, var(--ws-accent-strong) 46%, var(--ws-border));
  transform: translateY(-2px);
}

.ranking-podium__item--rank-1 {
  grid-column: 2;
}

.ranking-podium__item--rank-2 {
  grid-column: 1;
}

.ranking-podium__item--rank-3 {
  grid-column: 3;
}

.ranking-podium__item > .ranking-medal {
  z-index: 2;
  margin-bottom: -22px;
}

.ranking-podium__body {
  width: 100%;
  min-height: 106px;
  padding: 32px 12px 14px;
  text-align: center;
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--ws-surface-muted) 86%, transparent), color-mix(in srgb, var(--ws-table-inset-background) 92%, transparent));
  border: 1px solid var(--ws-border);
  border-bottom: 0;
  border-radius: var(--ws-radius) var(--ws-radius) 10px 10px;
  box-shadow: inset 0 1px 0 color-mix(in srgb, #ffffff 10%, transparent);
  transition: border-color 160ms ease, transform 160ms ease;
}

.ranking-podium__item--rank-1 .ranking-podium__body {
  min-height: 132px;
  padding-top: 36px;
}

.ranking-podium__item--rank-2 .ranking-podium__body {
  min-height: 116px;
}

.ranking-podium__item--rank-3 .ranking-podium__body {
  min-height: 100px;
}

.ranking-podium__value {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 4px;
  min-width: 0;
  color: var(--ws-accent-strong);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: clamp(1.2rem, 3vw, 1.9rem);
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.05em;
}

.ranking-podium__item--rank-1 .ranking-podium__value {
  font-size: clamp(1.35rem, 3.6vw, 2.35rem);
}

.ranking-podium__value small {
  overflow: hidden;
  color: var(--ws-text-muted);
  font-size: 0.58em;
  font-weight: 700;
  letter-spacing: -0.02em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ranking-podium__label {
  margin-top: 8px;
  overflow: hidden;
  color: var(--ws-text);
  font-size: 0.86rem;
  font-weight: 700;
  line-height: 1.2;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ranking-podium__caption {
  display: -webkit-box;
  margin-top: 5px;
  overflow: hidden;
  color: var(--ws-text-muted);
  font-size: 0.72rem;
  line-height: 1.25;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.ranking-podium__base {
  display: grid;
  place-items: center;
  width: 100%;
  height: 46px;
  color: var(--ws-text);
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--ws-accent-strong) 16%, var(--ws-surface-muted)), color-mix(in srgb, var(--ws-surface-muted) 84%, #000000 10%));
  border: 1px solid var(--ws-border);
  border-radius: 10px 10px var(--ws-radius) var(--ws-radius);
  box-shadow:
    inset 0 1px 0 color-mix(in srgb, #ffffff 12%, transparent),
    0 12px 24px color-mix(in srgb, #000000 12%, transparent);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 1.2rem;
  font-weight: 900;
}

.ranking-podium__item--rank-1 .ranking-podium__base {
  height: 66px;
  font-size: 1.55rem;
}

.ranking-podium__item--rank-2 .ranking-podium__base {
  height: 54px;
  font-size: 1.35rem;
}

.ranking-podium__item--rank-3 .ranking-podium__base {
  height: 42px;
}

.ranking-list {
  border-color: var(--ws-border);
  border-radius: var(--ws-radius);
  overflow: hidden;
  background: var(--ws-table-inset-background);
}

.ranking-list__caption {
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

@media (max-width: 520px) {
  .ranking-podium__stage {
    gap: 6px;
    min-height: 218px;
  }

  .ranking-podium__body {
    padding-right: 8px;
    padding-left: 8px;
  }

  .ranking-podium__value {
    flex-direction: column;
    gap: 2px;
  }

  .ranking-podium__label {
    font-size: 0.78rem;
  }
}
</style>
