<template>
  <div class="row q-col-gutter-xl">
    <div class="col-12 col-lg-6">
      <SectionCard title="Palabras">
        <TopRankingBoard v-if="topWords.length > 0" :items="topWords" unit="veces" />
        <p v-else class="text-muted">
          Sin palabras.
        </p>
      </SectionCard>
    </div>

    <div class="col-12 col-lg-6">
      <SectionCard title="Emojis">
        <TopRankingBoard v-if="topEmojis.length > 0" :items="topEmojis" unit="veces" />
        <p v-else class="text-muted">
          Sin emojis.
        </p>
      </SectionCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import SectionCard from 'components/common/SectionCard.vue';
import TopRankingBoard from 'components/results/TopRankingBoard.vue';
import type { DataPoint } from 'src/utils/records';

defineProps<{
  topWords: DataPoint[];
  topEmojis: DataPoint[];
}>();
</script>
