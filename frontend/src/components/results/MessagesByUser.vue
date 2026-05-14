<template>
  <SectionCard title="Mensajes por usuario">
    <div v-if="data.length === 0" class="text-muted">
      Sin datos.
    </div>

    <div v-else class="row q-col-gutter-lg">
      <div class="col-12 col-lg-8">
        <HorizontalBarChart :data="data" :height="chartHeight" />
      </div>

      <div class="col-12 col-lg-4">
        <RankingPodium :items="data" unit="mensajes" />
      </div>
    </div>
  </SectionCard>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import SectionCard from 'components/common/SectionCard.vue';
import HorizontalBarChart from 'components/common/HorizontalBarChart.vue';
import RankingPodium from 'components/results/RankingPodium.vue';
import type { DataPoint } from 'src/utils/records';

const props = defineProps<{
  data: DataPoint[];
}>();

const chartHeight = computed(() => Math.max(300, props.data.length * 38));
</script>
