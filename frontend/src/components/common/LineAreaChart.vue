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
  const isDark = $q.dark.isActive;
  const textColor = isDark ? '#f8fbff' : '#102033';
  const mutedColor = isDark ? '#9db1cc' : '#5f7189';
  const gridColor = isDark ? 'rgba(137,171,211,.14)' : 'rgba(72,98,132,.16)';
  const accentColor = isDark ? '#1597ff' : '#0b7cff';
  const pointColor = isDark ? '#8fcfff' : '#1597ff';
  const areaColor = isDark ? 'rgba(21,151,255,.14)' : 'rgba(11,124,255,.12)';

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
          {
            type: 'slider',
            height: 22,
            bottom: 10,
            borderColor: isDark ? 'rgba(137,171,211,.18)' : 'rgba(72,98,132,.16)',
            backgroundColor: isDark ? 'rgba(137,171,211,.08)' : 'rgba(72,98,132,.08)',
            fillerColor: isDark ? 'rgba(21,151,255,.22)' : 'rgba(11,124,255,.18)',
            handleStyle: { color: accentColor },
            textStyle: { color: mutedColor }
          }
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
          color: accentColor
        },
        itemStyle: {
          color: pointColor
        },
        areaStyle: {
          color: areaColor
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
