<template>
  <div class="temporal-activity">
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
      <LineAreaChart
        v-if="messagesPerDay.length > 0"
        :data="messagesPerDay"
        name="Mensajes por día"
        :height="340"
      />
      <p v-else class="text-muted">Sin días.</p>
    </SectionCard>

    <div class="temporal-activity__grid">
      <div class="temporal-activity__item">
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

      <div class="temporal-activity__item">
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
import SectionCard from 'components/common/SectionCard.vue';
import HorizontalBarChart from 'components/common/HorizontalBarChart.vue';
import LineAreaChart from 'components/common/LineAreaChart.vue';
import type { DataPoint } from 'src/utils/records';

defineProps<{
  hotHours: DataPoint[];
  messagesPerDay: DataPoint[];
  messagesPerMonth: DataPoint[];
  messagesPerYear: DataPoint[];
  topMessagesPerDay: DataPoint[];
}>();
</script>

<style scoped lang="scss">
.temporal-activity,
.temporal-activity__grid,
.temporal-activity__item {
  min-width: 0;
}

.temporal-activity {
  display: grid;
  gap: clamp(24px, 3vw, 36px);
  width: 100%;
  max-width: 100%;
  overflow-x: clip;
}

.temporal-activity__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(14px, 1.8vw, 22px);
  width: 100%;
  max-width: 100%;
  overflow: hidden;
}

.temporal-activity__item {
  max-width: 100%;
  overflow: hidden;
}

.temporal-activity__item :deep(.section-card) {
  height: 100%;
}

@media (max-width: 1024px) {
  .temporal-activity__grid {
    grid-template-columns: 1fr;
  }
}
</style>
