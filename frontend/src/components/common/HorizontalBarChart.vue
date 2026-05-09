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
  const isDark = $q.dark.isActive;
  const textColor = isDark ? '#f8fbff' : '#102033';
  const mutedColor = isDark ? '#9db1cc' : '#5f7189';
  const gridColor = isDark ? 'rgba(137,171,211,.14)' : 'rgba(72,98,132,.16)';
  const accentColor = isDark ? '#1597ff' : '#0b7cff';

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
          borderRadius: [0, 9, 9, 0],
          color: accentColor
        }
      }
    ]
  };
});
</script>
