<template>
  <SectionCard title="Mensajes por usuario">
    <div v-if="data.length === 0" class="text-muted">
      Sin datos.
    </div>

    <TopRankingBoard v-else :items="data" unit="mensajes" />
  </SectionCard>
</template>

<script setup lang="ts">
import SectionCard from 'components/common/SectionCard.vue';
import TopRankingBoard from 'components/results/TopRankingBoard.vue';
import type { DataPoint } from 'src/utils/records';

defineProps<{
  data: DataPoint[];
}>();
</script>
