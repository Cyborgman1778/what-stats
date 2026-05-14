<template>
  <SectionCard title="Rachas">
    <RankingPodium v-if="streakItems.length > 0" :items="streakItems" unit="días" />

    <p v-else class="text-muted">
      Sin rachas.
    </p>
  </SectionCard>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import SectionCard from 'components/common/SectionCard.vue';
import RankingPodium from 'components/results/RankingPodium.vue';
import type { TopStreak } from 'src/services/api/types';
import { formatIsoDate } from 'src/utils/dates';

const props = defineProps<{
  streaks: TopStreak[];
}>();

const streakItems = computed(() =>
  props.streaks.map((streak, index) => ({
    key: `${streak.start}-${streak.end}-${index}`,
    label: `${formatIsoDate(streak.start)} - ${formatIsoDate(streak.end)}`,
    value: streak.duration
  }))
);
</script>
