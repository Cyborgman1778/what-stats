<template>
  <v-chart class="chart-container" :option="option" autoresize />
</template>

<script setup lang="ts">
import type { EChartsOption } from 'echarts';
import { computed } from 'vue';
import { useQuasar } from 'quasar';

const props = defineProps<{
  title?: string;
  data: Record<string, number>;
  type: 'bar' | 'pie' | 'line';
  xAxisTitle?: string;
  horizontal?: boolean;
}>();

const $q = useQuasar();

const piePalette = ['#0f766e', '#0ea5e9', '#f59e0b', '#14b8a6', '#155e75', '#f97316', '#22c55e', '#334155'];

const option = computed<EChartsOption>(() => {
  const isDark = $q.dark.isActive;
  const textColor = isDark ? '#E2E8F0' : '#0F172A';
  const mutedTextColor = isDark ? '#94A3B8' : '#64748B';
  const primaryColor = '#0F766E';
  const secondaryColor = '#155E75';
  const splitLineColor = isDark ? 'rgba(148, 163, 184, 0.12)' : 'rgba(15, 23, 42, 0.08)';
  const axisLineColor = isDark ? 'rgba(148, 163, 184, 0.18)' : 'rgba(15, 23, 42, 0.12)';

  const entries = Object.entries(props.data);

  if (props.horizontal || props.type === 'pie') {
    entries.sort((a, b) => b[1] - a[1]);
  }

  const labels = entries.map(([label]) => label);
  const values = entries.map(([, value]) => value);
  const sharedOptions: EChartsOption = {
    animationDuration: 550,
    animationEasing: 'cubicOut',
    textStyle: {
      color: textColor,
      fontFamily: 'Manrope, sans-serif',
    },
    grid: {
      left: '4%',
      right: '4%',
      top: '6%',
      bottom: '6%',
      containLabel: true,
    },
  };

  if (props.type === 'bar') {
    const categoryLabels = props.horizontal ? [...labels].reverse() : labels;
    const seriesValues = props.horizontal ? [...values].reverse() : values;

    const barOption: EChartsOption = {
      ...sharedOptions,
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
          shadowStyle: {
            color: isDark ? 'rgba(148, 163, 184, 0.08)' : 'rgba(15, 23, 42, 0.04)',
          },
        },
      },
      xAxis: props.horizontal
        ? {
            type: 'value',
            axisLabel: { color: mutedTextColor },
            splitLine: { lineStyle: { color: splitLineColor } },
          }
        : {
            type: 'category',
            data: categoryLabels,
            axisLabel: {
              color: mutedTextColor,
              interval: 0,
              rotate: labels.length > 8 ? 28 : 0,
            },
            axisTick: { show: false },
            axisLine: { lineStyle: { color: axisLineColor } },
          },
      yAxis: props.horizontal
        ? {
            type: 'category',
            data: categoryLabels,
            axisLabel: { color: mutedTextColor },
            axisTick: { show: false },
            axisLine: { show: false },
          }
        : {
            type: 'value',
            axisLabel: { color: mutedTextColor },
            splitLine: { lineStyle: { color: splitLineColor } },
          },
      series: [
        {
          type: 'bar',
          data: seriesValues,
          barMaxWidth: 28,
          itemStyle: {
            color: props.horizontal ? secondaryColor : primaryColor,
            borderRadius: props.horizontal ? [0, 12, 12, 0] : [12, 12, 4, 4],
          },
        },
      ],
    };

    if (!props.horizontal && labels.length > 10) {
      barOption.dataZoom = [
        { type: 'inside' },
        {
          type: 'slider',
          bottom: 2,
          height: 18,
          borderColor: 'transparent',
          backgroundColor: isDark ? 'rgba(148, 163, 184, 0.08)' : 'rgba(15, 23, 42, 0.04)',
          fillerColor: isDark ? 'rgba(20, 184, 166, 0.22)' : 'rgba(15, 118, 110, 0.18)',
          moveHandleSize: 0,
        },
      ];
    }

    return barOption;
  }

  if (props.type === 'pie') {
    return {
      ...sharedOptions,
      color: piePalette,
      tooltip: { trigger: 'item' },
      legend: {
        show: entries.length <= 8,
        bottom: 0,
        textStyle: { color: mutedTextColor },
      },
      series: [
        {
          type: 'pie',
          radius: ['46%', '74%'],
          center: ['50%', '42%'],
          label: {
            color: mutedTextColor,
            formatter: '{b|{b}}\n{c}',
            rich: {
              b: {
                color: textColor,
                fontWeight: 700,
                lineHeight: 18,
              },
            },
          },
          labelLine: {
            lineStyle: { color: axisLineColor },
          },
          data: entries.slice(0, 15).map(([name, value]) => ({ name, value })),
          itemStyle: {
            borderRadius: 10,
            borderColor: isDark ? '#081622' : '#FFFFFF',
            borderWidth: 3,
          },
        },
      ],
    };
  }

  return {
    ...sharedOptions,
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: labels,
      axisLabel: { color: mutedTextColor },
      axisTick: { show: false },
      axisLine: { lineStyle: { color: axisLineColor } },
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: mutedTextColor },
      splitLine: { lineStyle: { color: splitLineColor } },
    },
    series: [
      {
        type: 'line',
        data: values,
        smooth: true,
        showSymbol: false,
        lineStyle: {
          color: primaryColor,
          width: 3,
        },
        areaStyle: {
          color: isDark ? 'rgba(20, 184, 166, 0.16)' : 'rgba(15, 118, 110, 0.12)',
        },
      },
    ],
  };
});
</script>

<style scoped>
.chart-container {
  height: 350px;
  width: 100%;
}
</style>
