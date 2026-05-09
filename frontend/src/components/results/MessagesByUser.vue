<template>
  <SectionCard
    title="Mensajes por usuario"
    subtitle="ranking"
  >
    <div v-if="data.length === 0" class="text-muted">
      Sin datos.
    </div>

    <div v-else class="row q-col-gutter-lg">
      <div class="col-12 col-lg-8">
        <HorizontalBarChart :data="data" :height="chartHeight" />
      </div>

      <div class="col-12 col-lg-4">
        <q-list bordered separator class="ranking-list">
          <q-item v-for="(item, index) in data" :key="item.label">
            <q-item-section avatar>
              <q-avatar color="primary" text-color="white" size="28px">
                {{ index + 1 }}
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label class="ellipsis">{{ item.label }}</q-item-label>
              <q-item-label caption>{{ formatNumber(item.value) }} mensajes</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </div>
  </SectionCard>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import SectionCard from 'components/common/SectionCard.vue';
import HorizontalBarChart from 'components/common/HorizontalBarChart.vue';
import type { DataPoint } from 'src/utils/records';
import { formatNumber } from 'src/utils/format';

const props = defineProps<{
  data: DataPoint[];
}>();

const chartHeight = computed(() => Math.max(300, props.data.length * 38));
</script>

<style scoped lang="scss">
.ranking-list {
  border-color: var(--ws-border);
  border-radius: var(--ws-radius);
  overflow: hidden;
  background: var(--ws-table-inset-background);
}
</style>
