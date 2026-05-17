<template>
  <v-chart
    v-if="data.length > 0"
    class="chart"
    :class="{ 'chart--noninteractive': props.compact }"
    :style="{ height: `${height}px` }"
    :option="option"
    autoresize
  />
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
    compact?: boolean;
    maxValue?: number;
  }>(),
  {
    height: 320,
    rankingMode: true,
    compact: false
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
    tooltip: props.compact
      ? { show: false }
      : {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          confine: true,
          valueFormatter: (value: number) => new Intl.NumberFormat('es-ES').format(value)
        },
    grid: {
      left: props.compact ? 0 : 12,
      right: props.compact ? 0 : 24,
      top: props.compact ? 10 : 12,
      bottom: props.compact ? 10 : 12,
      containLabel: !props.compact
    },
    xAxis: {
      type: 'value',
      max: props.maxValue,
      axisLabel: { show: !props.compact, color: mutedColor },
      axisTick: { show: false },
      axisLine: { show: false },
      splitLine: {
        show: !props.compact,
        lineStyle: {
          color: gridColor
        }
      }
    },
    yAxis: {
      type: 'category',
      data: source.map((item) => item.label),
      axisLabel: {
        show: !props.compact,
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
        silent: props.compact,
        barMaxWidth: props.compact ? 12 : 18,
        showBackground: props.compact,
        emphasis: {
          disabled: props.compact
        },
        backgroundStyle: {
          color: gridColor,
          borderRadius: [0, 999, 999, 0]
        },
        itemStyle: {
          borderRadius: [0, 999, 999, 0],
          color: accentColor
        }
      }
    ]
  };
});
</script>

<style scoped lang="scss">
.chart--noninteractive {
  pointer-events: none;
}
</style>
