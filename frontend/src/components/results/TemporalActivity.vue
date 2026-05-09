<template>
  <div class="q-gutter-xl">
    <SectionCard title="Horas" subtitle="actividad diaria">
      <LineAreaChart
        v-if="hotHours.length > 0"
        :data="hotHours"
        name="Mensajes por hora"
        :height="300"
      />
      <p v-else class="text-muted">Sin horas.</p>
    </SectionCard>

    <SectionCard
      title="Días"
      subtitle="serie diaria"
    >
      <div v-if="messagesPerDay.length > 0" class="chart-scroll">
        <div class="chart-scroll__inner" :style="{ minWidth: dailyMinWidth }">
          <LineAreaChart :data="messagesPerDay" name="Mensajes por día" :height="340" />
        </div>
      </div>
      <p v-else class="text-muted">Sin días.</p>
    </SectionCard>

    <div class="row q-col-gutter-xl">
      <div class="col-12 col-lg-6">
        <SectionCard title="Meses" subtitle="serie mensual">
          <LineAreaChart
            v-if="messagesPerMonth.length > 0"
            :data="messagesPerMonth"
            name="Mensajes por mes"
            :height="300"
          />
          <p v-else class="text-muted">Sin meses.</p>
        </SectionCard>
      </div>

      <div class="col-12 col-lg-6">
        <SectionCard title="Años" subtitle="serie anual">
          <LineAreaChart
            v-if="messagesPerYear.length > 0"
            :data="messagesPerYear"
            name="Mensajes por año"
            :height="300"
          />
          <p v-else class="text-muted">Sin años.</p>
        </SectionCard>
      </div>
    </div>

    <SectionCard title="Top días" subtitle="ranking">
      <HorizontalBarChart
        v-if="topMessagesPerDay.length > 0"
        :data="topMessagesPerDay"
        :height="Math.max(300, topMessagesPerDay.length * 36)"
      />
      <p v-else class="text-muted">Sin ranking.</p>
    </SectionCard>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import SectionCard from 'components/common/SectionCard.vue';
import HorizontalBarChart from 'components/common/HorizontalBarChart.vue';
import LineAreaChart from 'components/common/LineAreaChart.vue';
import type { DataPoint } from 'src/utils/records';

const props = defineProps<{
  hotHours: DataPoint[];
  messagesPerDay: DataPoint[];
  messagesPerMonth: DataPoint[];
  messagesPerYear: DataPoint[];
  topMessagesPerDay: DataPoint[];
}>();

const dailyMinWidth = computed(() => `${Math.max(760, props.messagesPerDay.length * 34)}px`);
</script>
