<template>
  <div class="row q-col-gutter-xl">
    <div class="col-12 col-lg-6">
      <SectionCard title="Palabras" subtitle="ranking">
        <HorizontalBarChart
          v-if="topWords.length > 0"
          :data="topWords"
          :height="Math.max(320, topWords.length * 32)"
        />
        <p v-else class="text-muted">
          Sin palabras.
        </p>
      </SectionCard>
    </div>

    <div class="col-12 col-lg-6">
      <SectionCard title="Emojis" subtitle="ranking">
        <HorizontalBarChart
          v-if="topEmojis.length > 0"
          :data="topEmojis"
          :height="Math.max(320, topEmojis.length * 32)"
        />
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
import type { DataPoint } from 'src/utils/records';

defineProps<{
  topWords: DataPoint[];
  topEmojis: DataPoint[];
}>();
</script>
