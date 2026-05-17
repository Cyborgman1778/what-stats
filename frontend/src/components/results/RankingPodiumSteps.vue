<template>
  <div
    v-if="podiumEntries.length > 0"
    class="ranking-podium-steps q-pa-md"
    :class="{ 'ranking-podium-steps--dark': $q.dark.isActive }"
  >
    <div class="ranking-podium-steps__stage flex items-end justify-center no-wrap">
      <article
        v-for="entry in podiumEntries"
        :key="getEntryKey(entry)"
        class="ranking-podium-steps__slot"
        :class="[
          `ranking-podium-steps__slot--rank-${entry.position}`,
          { 'ranking-podium-steps__slot--selectable': selectable }
        ]"
        :role="selectable ? 'button' : undefined"
        :tabindex="selectable ? 0 : undefined"
        @click="selectEntry(entry)"
        @keydown.enter.prevent="selectEntry(entry)"
        @keydown.space.prevent="selectEntry(entry)"
      >
        <div class="ranking-podium-steps__info text-center q-px-xs">
          <div class="ranking-podium-steps__name ellipsis">{{ entry.item.label }}</div>
          <div class="ranking-podium-steps__value">{{ getValueLabel(entry.item) }}</div>
          <div v-if="entry.item.caption" class="ranking-podium-steps__caption ellipsis">
            {{ entry.item.caption }}
          </div>
        </div>

        <div class="ranking-podium-steps__box">
          <div class="ranking-podium-steps__badge" aria-hidden="true">
            <svg class="ranking-podium-steps__medal" viewBox="0 0 96 96" focusable="false">
              <path
                d="M48 5.5c-18.4 0-33.3 14.9-33.3 33.3 0 9.2 3.7 17.5 9.8 23.5l-7.8 27.1 20.4-10 10.9 15 10.9-15 20.4 10-7.8-27.1c6.1-6 9.8-14.3 9.8-23.5C81.3 20.4 66.4 5.5 48 5.5Zm0 11.7c11.9 0 21.6 9.7 21.6 21.6S59.9 60.4 48 60.4 26.4 50.7 26.4 38.8 36.1 17.2 48 17.2Z"
              />
            </svg>
            <span class="ranking-podium-steps__rank">{{ entry.position }}</span>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useQuasar } from 'quasar';
import { formatNumber } from 'src/utils/format';

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
    selectable?: boolean;
  }>(),
  {
    unit: '',
    selectable: false
  }
);

const emit = defineEmits<{
  select: [entry: RankingEntry];
}>();

const $q = useQuasar();
const visualOrder = [2, 1, 3];

const podiumEntries = computed(() => {
  const topEntries = props.entries.slice(0, 3);

  return visualOrder
    .map((position) => topEntries.find((entry) => entry.position === position))
    .filter((entry): entry is RankingEntry => Boolean(entry));
});

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

function selectEntry(entry: RankingEntry) {
  if (!props.selectable) return;

  emit('select', entry);
}
</script>

<style scoped lang="scss">
.ranking-podium-steps {
  min-width: 0;
  overflow: hidden;
}

.ranking-podium-steps__stage {
  gap: 0;
  min-width: 0;
}

.ranking-podium-steps__slot {
  --podium-medal: #f4b84a;
  --podium-medal-soft: rgba(244, 184, 74, 0.3);
  --podium-border: color-mix(in srgb, var(--podium-medal) 45%, var(--ws-border));

  display: flex;
  width: min(31.8%, 172px);
  min-width: 0;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-end;
  color: var(--ws-text);
  outline: none;
}

.ranking-podium-steps__slot--selectable {
  cursor: pointer;
}

.ranking-podium-steps__slot--selectable:focus-visible .ranking-podium-steps__box,
.ranking-podium-steps__slot--selectable:hover .ranking-podium-steps__box {
  filter: brightness(1.08);
}

.ranking-podium-steps__slot--rank-1 {
  --podium-medal: #f7c948;
  --podium-medal-soft: rgba(247, 201, 72, 0.34);
  --podium-border: color-mix(in srgb, #f7c948 68%, var(--ws-border));
  z-index: 3;
}

.ranking-podium-steps__slot--rank-2 {
  --podium-medal: #aeb9c9;
  --podium-medal-soft: rgba(174, 185, 201, 0.32);
  --podium-border: color-mix(in srgb, #aeb9c9 62%, var(--ws-border));
  z-index: 1;
}

.ranking-podium-steps__slot--rank-3 {
  --podium-medal: #c9783f;
  --podium-medal-soft: rgba(201, 120, 63, 0.34);
  --podium-border: color-mix(in srgb, #c9783f 64%, var(--ws-border));
  z-index: 1;
}

.ranking-podium-steps__info {
  display: grid;
  min-height: 64px;
  align-content: end;
  gap: 3px;
  margin-bottom: 10px;
}

.ranking-podium-steps__name {
  color: var(--ws-text);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 0.88rem;
  font-weight: 800;
  line-height: 1.1;
}

.ranking-podium-steps__value {
  color: var(--podium-medal);
  font-size: 0.78rem;
  font-weight: 800;
  line-height: 1.1;
}

.ranking-podium-steps__caption {
  color: var(--ws-text-muted);
  font-size: 0.72rem;
  line-height: 1.1;
}

.ranking-podium-steps__box {
  position: relative;
  overflow: hidden;
  min-width: 0;
  background: color-mix(in srgb, var(--ws-surface-muted) 72%, var(--ws-surface-solid));
  border-top: 2px solid var(--podium-border);
  box-shadow:
    inset 0 1px 0 color-mix(in srgb, #ffffff 10%, transparent),
    0 14px 34px color-mix(in srgb, #000000 14%, transparent);
  transition: filter 160ms ease;
}

.ranking-podium-steps:not(.ranking-podium-steps--dark) .ranking-podium-steps__box {
  background: color-mix(in srgb, #ffffff 88%, var(--ws-surface-muted));
  box-shadow:
    inset 0 1px 0 color-mix(in srgb, #ffffff 72%, transparent),
    0 14px 34px color-mix(in srgb, #174064 10%, transparent);
}

.ranking-podium-steps__slot--rank-1 .ranking-podium-steps__box {
  height: 178px;
  border-right: 2px solid var(--podium-border);
  border-left: 2px solid var(--podium-border);
  border-radius: 24px 24px 0 0;
}

.ranking-podium-steps__slot--rank-2 .ranking-podium-steps__box {
  height: 132px;
  border-left: 2px solid var(--podium-border);
  border-radius: 24px 0 0 0;
}

.ranking-podium-steps__slot--rank-3 .ranking-podium-steps__box {
  height: 104px;
  border-right: 2px solid var(--podium-border);
  border-radius: 0 24px 0 0;
}

.ranking-podium-steps__badge {
  position: absolute;
  inset: 50% auto auto 50%;
  display: grid;
  width: clamp(68px, 8.8vw, 98px);
  aspect-ratio: 1;
  transform: translate(-50%, -50%);
}

.ranking-podium-steps__medal {
  display: block;
  width: 100%;
  height: 100%;
  color: var(--podium-medal);
  fill: currentColor;
  opacity: 0.5;
}

.ranking-podium-steps__rank {
  position: absolute;
  top: 40.5%;
  left: 50%;
  z-index: 1;
  color: color-mix(in srgb, var(--ws-text) 92%, transparent);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: clamp(1.28rem, 3vw, 2rem);
  font-weight: 800;
  line-height: 1;
  opacity: 0.96;
  transform: translate(-50%, -50%);
  text-shadow: none;
}

@media (max-width: 520px) {
  .ranking-podium-steps {
    padding-right: 0;
    padding-left: 0;
  }

  .ranking-podium-steps__slot {
    width: 33.333%;
  }

  .ranking-podium-steps__slot--rank-1 .ranking-podium-steps__box {
    height: 150px;
    border-radius: 18px 18px 0 0;
  }

  .ranking-podium-steps__slot--rank-2 .ranking-podium-steps__box {
    height: 112px;
    border-radius: 18px 0 0 0;
  }

  .ranking-podium-steps__slot--rank-3 .ranking-podium-steps__box {
    height: 88px;
    border-radius: 0 18px 0 0;
  }

  .ranking-podium-steps__info {
    min-height: 58px;
  }
}
</style>
