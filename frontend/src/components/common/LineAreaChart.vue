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
    name?: string;
  }>(),
  {
    height: 320,
    name: 'Mensajes'
  }
);

const $q = useQuasar();

const option = computed(() => {
  const manyPoints = props.data.length > 20;
  const textColor = $q.dark.isActive ? '#e6edf3' : '#1f2328';
  const mutedColor = $q.dark.isActive ? '#8b949e' : '#656d76';
  const gridColor = $q.dark.isActive ? 'rgba(48,54,61,.9)' : 'rgba(208,215,222,.9)';

  return {
    tooltip: {
      trigger: 'axis',
      valueFormatter: (value: number) => new Intl.NumberFormat('es-ES').format(value)
    },
    grid: {
      left: 10,
      right: 18,
      top: 18,
      bottom: manyPoints ? 52 : 24,
      containLabel: true
    },
    dataZoom: manyPoints
      ? [
          { type: 'inside', throttle: 40 },
          { type: 'slider', height: 22, bottom: 10 }
        ]
      : [],
    xAxis: {
      type: 'category',
      data: props.data.map((item) => item.label),
      boundaryGap: false,
      axisLabel: {
        color: mutedColor,
        rotate: props.data.length > 12 ? 35 : 0
      },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: mutedColor },
      splitLine: {
        lineStyle: {
          color: gridColor
        }
      }
    },
    series: [
      {
        name: props.name,
        type: 'line',
        smooth: true,
        symbolSize: 6,
        lineStyle: {
          width: 3,
          color: $q.dark.isActive ? '#3fb950' : '#1f883d'
        },
        itemStyle: {
          color: $q.dark.isActive ? '#2f81f7' : '#0969da'
        },
        areaStyle: {
          color: $q.dark.isActive ? 'rgba(63,185,80,.12)' : 'rgba(31,136,61,.1)'
        },
        data: props.data.map((item) => item.value)
      }
    ],
    textStyle: {
      color: textColor
    }
  };
});
</script>
