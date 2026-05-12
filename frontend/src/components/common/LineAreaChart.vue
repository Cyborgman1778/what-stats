<template>
  <v-chart v-if="data.length > 0" class="chart" :style="{ height: `${height}px` }" :option="option" autoresize />
</template>

<script setup lang="ts">
import { Capacitor } from '@capacitor/core';
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
const isNativeRuntime = Capacitor.isNativePlatform();

const option = computed(() => {
  const manyPoints = props.data.length > 20;
  const hasSparsePoints = props.data.length <= 4;
  const nativeMinValueSpan = isNativeRuntime
    ? Math.min(60, Math.max(4, Math.ceil(props.data.length * 0.04)))
    : undefined;
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
      confine: true,
      ...(isNativeRuntime
        ? {
            triggerOn: 'mousemove|click',
            axisPointer: {
              type: 'line',
              snap: true,
              lineStyle: {
                color: accentColor,
                width: 2
              },
              label: {
                show: true,
                color: '#ffffff',
                backgroundColor: accentColor
              }
            },
            hideDelay: 900
          }
        : {}),
      valueFormatter: (value: number) => new Intl.NumberFormat('es-ES').format(value)
    },
    grid: {
      left: 10,
      right: 18,
      top: 18,
      bottom: manyPoints ? (isNativeRuntime ? 88 : 52) : 24,
      containLabel: true
    },
    dataZoom: manyPoints
      ? [
          {
            type: 'inside',
            throttle: isNativeRuntime ? 120 : 40,
            moveOnMouseMove: !isNativeRuntime,
            moveOnMouseWheel: false,
            preventDefaultMouseMove: !isNativeRuntime,
            minValueSpan: nativeMinValueSpan
          },
          {
            type: 'slider',
            height: isNativeRuntime ? 44 : 22,
            bottom: isNativeRuntime ? 16 : 10,
            minValueSpan: nativeMinValueSpan,
            borderColor: isDark ? 'rgba(137,171,211,.18)' : 'rgba(72,98,132,.16)',
            backgroundColor: isDark ? 'rgba(137,171,211,.08)' : 'rgba(72,98,132,.08)',
            fillerColor: isDark ? 'rgba(21,151,255,.22)' : 'rgba(11,124,255,.18)',
            handleSize: isNativeRuntime ? 32 : undefined,
            moveHandleSize: isNativeRuntime ? 28 : undefined,
            handleStyle: {
              color: accentColor,
              borderColor: '#ffffff',
              borderWidth: isNativeRuntime ? 2 : 0,
              shadowBlur: isNativeRuntime ? 10 : 0,
              shadowColor: 'rgba(21,151,255,.32)'
            },
            moveHandleStyle: { color: accentColor },
            selectedDataBackground: {
              lineStyle: { color: accentColor },
              areaStyle: { color: areaColor }
            },
            textStyle: { color: mutedColor },
            showDetail: false,
            brushSelect: isNativeRuntime ? false : undefined
          }
        ]
      : [],
    xAxis: {
      type: 'category',
      data: props.data.map((item) => item.label),
      boundaryGap: hasSparsePoints,
      axisLabel: {
        color: mutedColor,
        hideOverlap: true,
        interval: manyPoints ? 'auto' : 0,
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
        sampling: manyPoints ? 'lttb' : undefined,
        showSymbol: props.data.length <= 28,
        symbolSize: props.data.length <= 12 ? 7 : 5,
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
