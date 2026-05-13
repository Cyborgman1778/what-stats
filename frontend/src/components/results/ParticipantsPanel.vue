<template>
  <SectionCard title="Participantes">
    <div v-if="participants.length > 0" class="participants-grid">
      <q-chip
        v-for="participant in participants"
        :key="participant"
        class="ws-chip participant-chip"
        icon="person"
      >
        <span class="ellipsis">{{ participant }}</span>
      </q-chip>
    </div>

    <div v-else class="text-muted">
      Sin participantes.
    </div>
  </SectionCard>
</template>

<script setup lang="ts">
import SectionCard from 'components/common/SectionCard.vue';

defineProps<{
  participants: string[];
}>();
</script>

<style scoped lang="scss">
.participants-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.participant-chip {
  max-width: 100%;
}
</style>
