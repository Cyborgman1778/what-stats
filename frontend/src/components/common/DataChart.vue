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

const piePalette = ['#1597ff', '#33a9ff', '#7cc8ff', '#2f6dff', '#8fcfff', '#5f7189', '#f4b84a', '#d7263d'];

const option = computed<EChartsOption>(() => {
  const isDark = $q.dark.isActive;
  const textColor = isDark ? '#f8fbff' : '#102033';
  const mutedTextColor = isDark ? '#9db1cc' : '#5f7189';
  const primaryColor = isDark ? '#1597ff' : '#0b7cff';
  const secondaryColor = isDark ? '#33a9ff' : '#0969da';
  const splitLineColor = isDark ? 'rgba(137, 171, 211, 0.14)' : 'rgba(72, 98, 132, 0.16)';
  const axisLineColor = isDark ? 'rgba(137, 171, 211, 0.18)' : 'rgba(72, 98, 132, 0.16)';

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
            color: isDark ? 'rgba(137, 171, 211, 0.08)' : 'rgba(72, 98, 132, 0.06)',
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
          backgroundColor: isDark ? 'rgba(137, 171, 211, 0.08)' : 'rgba(72, 98, 132, 0.06)',
          fillerColor: isDark ? 'rgba(21, 151, 255, 0.22)' : 'rgba(11, 124, 255, 0.18)',
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
            borderColor: isDark ? '#08162b' : '#ffffff',
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
          color: isDark ? 'rgba(21, 151, 255, 0.16)' : 'rgba(11, 124, 255, 0.12)',
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
