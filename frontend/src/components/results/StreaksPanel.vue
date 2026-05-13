<template>
  <SectionCard title="Rachas">
    <div v-if="streaks.length > 0" class="row q-col-gutter-md">
      <div v-for="(streak, index) in streaks" :key="`${streak.start}-${streak.end}-${index}`" class="col-12 col-md-4">
        <q-card flat class="streak-card">
          <q-card-section>
            <div class="row items-center justify-between">
              <q-avatar color="primary" text-color="white" size="30px">
                {{ index + 1 }}
              </q-avatar>

              <q-chip class="ws-chip" icon="local_fire_department">
                {{ streak.duration }} días
              </q-chip>
            </div>

            <div class="streak-card__dates q-mt-md">
              <div>
                <div class="text-muted">Inicio</div>
                <div class="text-weight-bold">{{ formatIsoDate(streak.start) }}</div>
              </div>

              <q-icon name="east" class="text-muted" />

              <div>
                <div class="text-muted">Fin</div>
                <div class="text-weight-bold">{{ formatIsoDate(streak.end) }}</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <p v-else class="text-muted">
      Sin rachas.
    </p>
  </SectionCard>
</template>

<script setup lang="ts">
import SectionCard from 'components/common/SectionCard.vue';
import type { TopStreak } from 'src/services/api/types';
import { formatIsoDate } from 'src/utils/dates';

defineProps<{
  streaks: TopStreak[];
}>();
</script>

<style scoped lang="scss">
.streak-card {
  height: 100%;
  border-radius: var(--ws-radius);
  background: var(--ws-table-inset-background);
  border: 1px solid var(--ws-border);
}

.streak-card__dates {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
</style>
