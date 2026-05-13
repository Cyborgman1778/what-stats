<template>
  <q-card flat class="metric-card">
    <q-card-section>
      <div class="metric-card__head">
        <span>{{ eyebrow }}</span>
        <q-icon :name="icon" size="18px" />
      </div>

      <div class="metric-card__value">{{ value }}</div>
      <div v-if="label" class="metric-card__label">{{ label }}</div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
defineProps<{
  icon: string;
  eyebrow: string;
  value: string | number;
  label?: string;
}>();
</script>

<style scoped lang="scss">
.metric-card {
  height: 100%;
  overflow: hidden;
  background: var(--ws-metric-card-background);
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  box-shadow: var(--ws-shadow);
}

.metric-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--ws-text-muted);
  font-size: 0.8rem;
  font-weight: 600;
}

.metric-card__head .q-icon {
  color: var(--ws-accent-strong);
}

.metric-card__value {
  margin-top: 18px;
  color: var(--ws-accent-strong);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: clamp(1.75rem, 3vw, 2.3rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.04em;
}

.metric-card__label {
  margin-top: 7px;
  color: var(--ws-text-muted);
  font-size: 0.84rem;
}
</style>
