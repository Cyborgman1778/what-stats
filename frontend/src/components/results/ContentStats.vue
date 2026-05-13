<template>
  <div class="row q-col-gutter-xl">
    <div class="col-12 col-lg-6">
      <SectionCard title="Palabras">
        <div v-if="topWords.length > 0" class="content-ranking">
          <HorizontalBarChart
            :data="topWords"
            :height="Math.max(320, topWords.length * 32)"
          />

          <RankingList :data="topWords" unit="veces" />
        </div>
        <p v-else class="text-muted">
          Sin palabras.
        </p>
      </SectionCard>
    </div>

    <div class="col-12 col-lg-6">
      <SectionCard title="Emojis">
        <div v-if="topEmojis.length > 0" class="content-ranking">
          <HorizontalBarChart
            :data="topEmojis"
            :height="Math.max(320, topEmojis.length * 32)"
          />

          <RankingList :data="topEmojis" unit="veces" />
        </div>
        <p v-else class="text-muted">
          Sin emojis.
        </p>
      </SectionCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import SectionCard from 'components/common/SectionCard.vue';
import HorizontalBarChart from 'components/common/HorizontalBarChart.vue';
import RankingList from 'components/results/RankingList.vue';
import type { DataPoint } from 'src/utils/records';

defineProps<{
  topWords: DataPoint[];
  topEmojis: DataPoint[];
}>();
</script>

<style scoped lang="scss">
.content-ranking {
  display: grid;
  gap: 18px;
}
</style>
