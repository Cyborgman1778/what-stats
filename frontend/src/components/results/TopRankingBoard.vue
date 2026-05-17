<template>
  <div class="top-ranking-board">
    <RankingPodiumSteps
      :entries="rankedEntries"
      :unit="normalizedUnit"
      :selectable="isSelectable"
      @select="emit('select', $event.item, $event.position)"
    />

    <RankingRemainderList
      v-if="listEntries.length > 0"
      :entries="listEntries"
      :unit="normalizedUnit"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import RankingPodiumSteps from 'components/results/RankingPodiumSteps.vue';
import RankingRemainderList from 'components/results/RankingRemainderList.vue';

interface TopRankingItem {
  key?: string | number;
  label: string;
  value: string | number;
  caption?: string;
}

interface TopRankingEntry {
  item: TopRankingItem;
  position: number;
}

const props = withDefaults(
  defineProps<{
    items: TopRankingItem[];
    unit?: string;
    selectable?: boolean;
  }>(),
  {
    unit: '',
    selectable: false
  }
);

const emit = defineEmits<{
  select: [item: TopRankingItem, position: number];
}>();

const rankedEntries = computed<TopRankingEntry[]>(() =>
  props.items.map((item, index) => ({
    item,
    position: index + 1
  }))
);

const normalizedUnit = computed(() => props.unit ?? '');
const isSelectable = computed(() => props.selectable ?? false);
const listEntries = computed(() => rankedEntries.value.slice(3));
</script>

<style scoped lang="scss">
.top-ranking-board {
  display: grid;
  gap: 18px;
  min-width: 0;
}
</style>
