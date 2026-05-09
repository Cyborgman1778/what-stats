<template>
  <v-chart v-if="data.length > 0" class="chart" :style="{ height: `${height}px` }" :option="option" autoresize />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useQuasar } from 'quasar';
import type { DataPoint } from 'src/utils/records';

const props = withDefaults(
  defineProps<{
    data: DataPoint[];
    height?: number;
    rankingMode?: boolean;
  }>(),
  {
    height: 320,
    rankingMode: true
  }
);

const $q = useQuasar();

const option = computed(() => {
  const source = props.rankingMode ? [...props.data].reverse() : props.data;
  const textColor = $q.dark.isActive ? '#e6edf3' : '#1f2328';
  const mutedColor = $q.dark.isActive ? '#8b949e' : '#656d76';
  const gridColor = $q.dark.isActive ? 'rgba(48,54,61,.9)' : 'rgba(208,215,222,.9)';

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      valueFormatter: (value: number) => new Intl.NumberFormat('es-ES').format(value)
    },
    grid: {
      left: 12,
      right: 24,
      top: 12,
      bottom: 12,
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: { color: mutedColor },
      splitLine: {
        lineStyle: {
          color: gridColor
        }
      }
    },
    yAxis: {
      type: 'category',
      data: source.map((item) => item.label),
      axisLabel: {
        color: textColor,
        width: 150,
        overflow: 'truncate'
      },
      axisTick: { show: false },
      axisLine: { show: false }
    },
    series: [
      {
        type: 'bar',
        data: source.map((item) => item.value),
        barMaxWidth: 18,
        itemStyle: {
          borderRadius: [0, 4, 4, 0],
          color: $q.dark.isActive ? '#3fb950' : '#1f883d'
        }
      }
    ]
  };
});
</script>
